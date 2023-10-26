[MMRL]: https://github.com/DerGoogler/MMRL

# Googlers Magisk Repo

These are for [MMRL][MMRL]. Modules that don't include a `META-INF` folder will be removed from the API. These modules mostly not installable or causes problems to the end-user.

Your module `last_updated` will be updated when you change something in the `module.prop`

- [Magisk Modules Alt Repo](https://api.mmrl.dergoogler.com/json/mmar.json)
- [Googlers Repo](https://api.mmrl.dergoogler.com/json/gmr.json)
- [Magisk Modules Official Repo](https://api.mmrl.dergoogler.com/json/mmr.json)

## Use your `update.json`

[MMRL][MMRL] and repos generated with this script can use their own `update.json`, but it still depends on the hourly updates.

> Do not write `versionCode` as a `string`, please write it as a `number`.

```json
{
    "version": "1.36.1",
    "versionCode": 13614,
    "zipUrl": "https://forum.xda-developers.com/attachments/update-busybox-installer-v1-36-1-all-signed-zip.6000117/",
    "changelog": "https://raw.githubusercontent.com/Magisk-Modules-Repo/busybox-ndk/master/README.md"
}
```

## Configure your module page in [MMRL][MMRL]

[MMRL][MMRL] allows you to configure:

- `logo` - url (string)
- `cover` - url (string)
- `screenshots` - url (array)
- `categories` - please see [`useCategories.ts`](https://github.com/DerGoogler/MMRL/blob/master/Website/src/hooks/useCategories.ts) which categories are available
- `require` - module id (array)

Example

> You'll have to create `mmrl.json` file to use these features
> `require` will only work if a repo is added which contains the module

```json
{
    "logo": "https://github.com/DerGoogler/MMRL/blob/master/Android/app/src/main/ic_launcher-playstore.png?raw=true",
    "cover": "https://mmrl.dergoogler.com/assets/MMRL-Cover.png",
    "screenshots": [
        "https://github.com/Googlers-Repo/googlers-repo.github.io/assets/54764558/f5b7d396-781e-463a-b4ed-dc345cc15ba3I",
        "https://github.com/Googlers-Repo/googlers-repo.github.io/assets/54764558/0a03c54a-3064-4ed0-a69b-90db437bd9f0",
        "https://github.com/Googlers-Repo/googlers-repo.github.io/assets/54764558/8fbc9621-fe85-4b66-8070-271599f87d38"
    ],
    "categories": [
        "Tools",
        "System",
        "Configurable"
    ],
    "require": [
        "mkshrc",
        "gcc_on_android"
    ]
}
```