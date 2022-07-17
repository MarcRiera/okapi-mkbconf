# okapi-mkbconf

Python script to create BCONF files for [Okapi Framework](https://okapiframework.org) from a folder. This allows creating and updating configurations easily without Okapi Rainbow. 

## Usage

Simply pass the path to the folder containing the extracted configuration as the first argument:

`okapi-makebconf.py <folder>`

## Supported features

* Pipeline (`pipeline.pln`)
* Custom filters (`*.frpm`)
* Extension mappings (`extensions-mapping.txt`): tab-separated text file with extension-filter mappings, one per line.

## Pending features

* Plugins (they are currently ignored and not packaged)
* Referenced external files (same as plugins)
