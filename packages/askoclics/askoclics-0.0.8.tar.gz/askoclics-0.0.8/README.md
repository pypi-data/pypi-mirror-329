# Askoclics

[AskOmics](https://github.com/askomics/flaskomics) server.


```bash
# On first use you'll need to create a config file to connect to the server, just run:

$ askoclics init
Welcome to Askoclics
Askomics server url, including http:// and the port if required: http://0.0.0.0:80
Askomics user's API key: XXXXXXX
Testing connection...
Ok! Everything looks good.
Ready to go! Type `askoclics` to get a list of commands you can execute.

```

This will create an askoclic config file in ~/.askoclics.yml

## Examples

```bash

# List all files
$ askoclics file list
[
    {
        "name": "qtl.tsv",
        "size": 99,
        "type": "csv/tsv",
        "id": 2,
        "date": 1612957604
    },
    {
        "name": "gene.gff3",
        "size": 2267,
        "type": "gff/gff3",
        "id": 3,
        "date": 1612957604
    },
    {
        "name": "gene.bed",
        "size": 689,
        "type": "bed",
        "id": 4,
        "date": 1612957604
    }
]










```

## License

Available under the MIT License
