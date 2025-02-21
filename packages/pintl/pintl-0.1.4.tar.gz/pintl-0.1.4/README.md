# PIntl

PIntl is a localization package heavily inspired by the Flutter's "intl" package. The localization files are in ".arb" format (basically json), one file per language in a single folder.

## Usage

To use PIntl, first initialize the localization

```PIntl.load("tests/l10n")```
or 
if you need per instance localization, like in web service
```pintl = PIntl.load("tests/l10n")``` 

and set the locale:
```set_locale("fi")```
or
```pintl.set_locale("fi")```

####

To get the string, simply call global string function (uses last created instance) with optional parameter dictionary:
```_("my_localized_string", {"param1",123})```

or equivalent instance method
```_("my_localized_string", {"param1",123})```


