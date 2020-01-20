# Beancount Extra

My tools for automating [Beancount][beancount-home].

[beancount-home]: http://furius.ca/beancount/

## Importers

### PDF Statement Importers

#### Motivation

- <b>Why do we need to import from PDF statements?</b>
  <br>Banks normally will only allow you to export OFX files within a limited time span (1-2 yrs) and the narriation provided in the OFX format is usually truncated. PDF statements contains a lot of useful information.

- <b>Which PDF table processing library do you use?</b>
   <br>I use [Camelot][camelot-docs]. Camelot uses PDFMiner. Camelot allows the cumbersome job of PDF processing to be largely automated.

[camelot-docs]: https://camelot-py.readthedocs.io/en/master/

#### List of Importers

- Bank of America PDF Deposite Statement Importer
- Bank of America PDF Credit Statement Importer
- Chase PDF Statement Importer

#### Known Issues

- Unable to recognize account number automatically.
- Unable to set the year correctly.
- Need to implement a formal way to extract / set file date.
- Need to implement a common interface.

### Venmo Importers

- Venmo CSV Importer

## Additional Resources

- Plain text accounting [in general][plaintextaccounting-org]
- Beancount's [official documentation][official-doc] an its [unofficial take][generated-doc]
- Source code on [GitHub][beancount-github] and [Bitbucket][beancount-bitbucket]

[plaintextaccounting-org]: https://plaintextaccounting.org
[official-doc]: http://furius.ca/beancount/doc/index
[generated-doc]: https://xuhcc.github.io/beancount-docs/
[beancount-bitbucket]: https://bitbucket.org/blais/beancount/src
[beancount-github]: https://github.com/beancount/beancount
