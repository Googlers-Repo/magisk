mkdir -p $TMPDIR/$REPO_SCOPE/modules
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
    cd $TMPDIR/$REPO_SCOPE/archives/$id/unzipped/*/
    zip -r "$TMPDIR/$REPO_SCOPE/modules/$id-$version.zip" *
    cd "$OLDPWD"

    TAG_NAME="${REPO_SCOPE^^}-Releases"
    echo "Using $TAG_NAME for releases"

    if [ -f "$TMPDIR/$REPO_SCOPE/modules/$id-$version.zip" ]; then
        hub release create -a "$TMPDIR/$REPO_SCOPE/modules/$id-$version.zip" -m "$TAG_NAME" "$TAG_NAME"
    else
        echo "Unable to find $TMPDIR/$REPO_SCOPE/modules/$id-$version.zip"
    fi

done < <( cat "$REPO_SCOPE.json" | jq -r '.modules[] | .id, .download, .version' )