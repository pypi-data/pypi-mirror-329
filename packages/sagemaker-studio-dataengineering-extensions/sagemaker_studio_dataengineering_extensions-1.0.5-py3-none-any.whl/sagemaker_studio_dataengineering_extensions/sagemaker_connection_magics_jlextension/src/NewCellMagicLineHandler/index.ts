import {JupyterFrontEnd,
  type JupyterFrontEndPlugin,
  LabShell
} from '@jupyterlab/application';
import {ISettingRegistry} from "@jupyterlab/settingregistry";
import {Constants} from "../constants";
import {
  createNewCellSourceForCell,
  getCachedConnection,
  getCachedInterpreter,
  getDefaultConnection,
  getDefaultInterpreter,
  isCellStartWithSupportedMagics,
  isSageMakerConnectionSupportedForNotebook,
  isNewSageMakerSupportedNotebook,
  setCachedConnectionAndLanguage,
  setSettingUserSelection
} from "../utils/DropdownUtils";
import {NotebookPanel} from "@jupyterlab/notebook";
import {ICellModel} from "@jupyterlab/cells";
import {getMainPanels} from "../utils";


export const handleCellAdd = (panel: NotebookPanel,
                              cell: ICellModel | undefined, newNotebook: boolean) => {
  const notebookModel = panel.model
  if (notebookModel === null) {
    console.warn("Notebook model is null. skipping handle cell add")
    return
  }
  const connectionName = newNotebook ? getDefaultConnection() : getCachedConnection()
  const interpreterName = newNotebook ? getDefaultInterpreter() : getCachedInterpreter()
  if (connectionName == Constants.DEFAULT_IAM_CONNECTION_NAME && interpreterName == Constants.INTERPRETER_LOCAL_PYTHON_VALUE) {
    return;
  }
  const cellContent = cell?.sharedModel.source
  if (cellContent != undefined && !isCellStartWithSupportedMagics(cellContent)) {
    const newSource = createNewCellSourceForCell(interpreterName, connectionName, cellContent);
    cell?.sharedModel.setSource(newSource)
  }
}

export const newCellMagicLineHandler: JupyterFrontEndPlugin<void> = {
  id: '@amzn/sagemaker-connection-magics-jlextension:default-connection-toolbar',
  requires: [ISettingRegistry],
  autoStart: true,
  activate: (app: JupyterFrontEnd, settings: ISettingRegistry) => {
    console.log('sagemaker-connection-magics-jlextension:default-connection-toolbar is activated!');
    const notebookPanels = new Set<string>();
    prepareForNewCell()
    function loadSetting(setting: ISettingRegistry.ISettings): void {
      const connection = setting.get(Constants.USER_SETTING_CONNECTION_KEY).composite as string;
      const language = setting.get(Constants.USER_SETTING_LANGUAGE_KEY).composite as string;
      const interpreter = setting.get(Constants.USER_SETTING_INTERPRETER_KEY).composite as string;
      setSettingUserSelection(Constants.USER_SETTING_CONNECTION_KEY, connection)
      setSettingUserSelection(Constants.USER_SETTING_LANGUAGE_KEY, language)
      setSettingUserSelection(Constants.USER_SETTING_INTERPRETER_KEY, interpreter)
    }

    async function prepareForNewCell(): Promise<void> {
      if (app.shell instanceof LabShell) {
        await app.shell.restored;
        const mainNotebookPanels = getMainPanels(app);
        mainNotebookPanels.forEach(notebookPanel => {
          notebookPanels.add(notebookPanel.id)
          handleCellAddOnCellsOrKernelChange(notebookPanel)
        });
        app.shell.activeChanged.connect((sender, changed) => {
          const notebookPanel = changed.newValue;
          if (notebookPanel && notebookPanel instanceof NotebookPanel) {
            if (notebookPanels.has(notebookPanel.id)) return
            notebookPanels.add(notebookPanel.id)
            handleCellAddOnCellsOrKernelChange(notebookPanel)
          }
        });
      }
    }

    function handleCellAddOnCellsOrKernelChange(notebookPanel: NotebookPanel): void {
      notebookPanel.model?.cells.changed.connect((cellList, cell) => {
        if (cell.type != "add") return
        if (!isSageMakerConnectionSupportedForNotebook(notebookPanel)) return;
        handleCellAdd(notebookPanel, cellList.get(cell.newIndex), cellList.length == 1)
      })
      notebookPanel.sessionContext.kernelChanged.connect((sessionContext, kernel) => {
        if (isNewSageMakerSupportedNotebook(kernel.newValue?.name, notebookPanel)) {
          handleCellAdd(notebookPanel, notebookPanel.model?.cells.get(0), true)
        }
      })
      notebookPanel.content.modelContentChanged.connect((notebook) => {
        setCachedConnectionAndLanguage(notebook.activeCell)
      })
      notebookPanel.content.activeCellChanged.connect((notebook, cell) => {
        setCachedConnectionAndLanguage(cell)
      })
      notebookPanel.disposed.connect(() => {
        notebookPanels.delete(notebookPanel.id)
      })
    }

    Promise.all([app.restored, settings.load(Constants.SAGEMAKER_JUPYTER_PLUGIN_SETTINGS_ID)])
      .then(([, setting]) => {
        loadSetting(setting);
        setting.changed.connect(loadSetting);
      })
      .catch(reason => {
        console.error(
          `Something went wrong when reading the settings.\n${reason}`
        );
      });
  }
};