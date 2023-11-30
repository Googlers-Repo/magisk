[MMRL]: https://github.com/DerGoogler/MMRL

# Googlers Magisk Repo

These are for [MMRL][MMRL]. Modules that don't include a `META-INF` folder will be removed from the API. These modules mostly not installable or causes problems to the end-user.

Your module `last_updated` will be updated when you change something in the `module.prop`

- [Magisk Modules Alt Repo](https://gr.dergoogler.com/magisk/mmar.json)
- [Googlers Repo](https://gr.dergoogler.com/magisk/gmr.json)
- [Magisk Modules Official Repo](https://gr.dergoogler.com/magisk/mmr.json)

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

- `author` - github username (string)
- `contributors` - github usernames (array)
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
    "author": "DerGoogler",
    "contributors": ["vhqtvn", "coder"],
    "logo": "https://avatars.githubusercontent.com/u/95932066?s=200&v=4",
    "cover": "https://coder.com/og-image.png",
    "screenshots": [
        "https://raw.githubusercontent.com/coder/code-server/main/docs/assets/screenshot-1.png",
        "https://raw.githubusercontent.com/coder/code-server/main/docs/assets/screenshot-2.png"
    ],
    "categories": [
        "Tools",
        "Customization",
        "Miscellaneous"
    ],
    "require": ["mkshrc", "node_on_android"]
}
```

## Usage of modules in others repos

Modules that are managed by **Googlers Repo**, **Der_Googler (DerGoogler)** etc are not allowed to show up in other repos. A exception for this rule is [**Magisk Modules Alt Repo**](https://github.com/Magisk-Modules-Alt-Repo), other repos are not allowed to host our modules.

> Mirrors of the [**Magisk Modules Alt Repo**](https://github.com/Magisk-Modules-Alt-Repo) are NOT an exception

## Request a module verification

Module verification request currently aren't open.

## Request a developer verification

Developer verification request currently aren't open.
