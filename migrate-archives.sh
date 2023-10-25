PWD=$(pwd)
TMPDIR="$PWD/tmp"
while read -r id ; do
    read -r download
    read -r version

    echo "Make dirs"
    mkdir -p $TMPDIR/$REPO_SCOPE/archives/$id/unzipped
    
    echo "Downloading $id"
    curl -L "$download" --output "$TMPDIR/$REPO_SCOPE/archives/$id/$id.zip"

    echo "Decompress $id"
    unzip -qq $TMPDIR/$REPO_SCOPE/archives/$id/$id.zip -d $TMPDIR/$REPO_SCOPE/archives/$id/unzipped

    echo "Recompress to a valid module"
    # Run ina subshell to keep the cwd
    mkdir -p "$PWD/modules/$REPO_SCOPE/$id"
    (cd $TMPDIR/$REPO_SCOPE/archives/$id/unzipped/*/ && zip -9 -qq -r "$PWD/modules/$REPO_SCOPE/$id/$version.zip" *)
done < <( cat "$REPO_SCOPE.json" | jq -r '.modules[] | .id, .download, .version' )
