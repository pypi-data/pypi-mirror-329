#!/bin/bash

# File path
INIT_FILE="src/sagemaker_studio_dataengineering_extensions/__init__.py"

# Get current date in YYYYMMDD format
CURRENT_DATE=$(date +"%Y%m%d")

# Extract current version from __init__.py
CURRENT_VERSION=$(grep "__version__" "$INIT_FILE" | cut -d'"' -f2)

# Function to generate new build number
generate_build_number() {
    local date=$1
    local current_build=$2
    
    if [ "$date" = "$CURRENT_DATE" ]; then
        # Same day, increment build number
        printf "%s%02d" "$date" $((10#$current_build + 1))
    else
        # New day, reset build number
        echo "${CURRENT_DATE}01"
    fi
}

# Check if current version has a build number
if [[ $CURRENT_VERSION =~ ^([0-9]+\.[0-9]+\.[0-9]+)\.([0-9]{10})$ ]]; then
    # Version with build number
    BASE_VERSION="${BASH_REMATCH[1]}"
    BUILD_DATE="${BASH_REMATCH[2]:0:8}"
    BUILD_NUMBER="${BASH_REMATCH[2]:8:2}"
    
    NEW_BUILD=$(generate_build_number "$BUILD_DATE" "$BUILD_NUMBER")
    NEW_VERSION="${BASE_VERSION}.${NEW_BUILD}"
else
    # Version without build number
    NEW_VERSION="${CURRENT_VERSION}.${CURRENT_DATE}01"
fi

# Update __init__.py with new version
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s/__version__=\".*\"/__version__=\"$NEW_VERSION\"/" "$INIT_FILE"
else
    # Linux and others
    sed -i "s/__version__=\".*\"/__version__=\"$NEW_VERSION\"/" "$INIT_FILE"
fi

echo "Version updated from $CURRENT_VERSION to $NEW_VERSION in $INIT_FILE"

# Optional: Display the updated line
# grep "__version__" "$INIT_FILE"