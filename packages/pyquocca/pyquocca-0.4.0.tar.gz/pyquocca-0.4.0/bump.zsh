#!/usr/bin/env zsh

cd $(dirname "$0")

version=$(yq '.project.version' pyproject.toml)
echo "Using version $version for pyquocca packages..."

# Update parent module challenges
cd ../../../challenges

for file in **/requirements.txt; do
    old=$(grep "^pyquocca" $file)
    if [[ -n $old ]]; then
        current_version=$(echo $old | grep -oE '==(.*)' | cut -d'=' -f3)

        if [[ $current_version == $version ]]; then
            echo $(dirname $file): up to date
        else
            echo $(dirname $file): updating $old '->' $version
            # Match pyquocca with optional extras, followed by any version
            sed -E -i '' '/^pyquocca(\[[^]]*\])?==.*/s//pyquocca\1=='$version'/' $file
        fi
    else
        echo $(dirname $file): no pyquocca requirement
    fi
done
