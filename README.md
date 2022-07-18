# Beancount Extra

My tools for automating [Beancount][beancount-home].

[beancount-home]: http://furius.ca/beancount/

## Importers

### PDF Statement Importers

#### Motivation

- <b>Why do you need to import from PDF statements?</b>
  <br>Banks normally will only allow me to export OFX files within a limited time span (1-2 yrs) and the narriations provided in the OFX format is usually truncated. However, PDF statements are usually archived and downloadable and the narrations are usually complete.

- <b>Which PDF table processing library do you use?</b>
   <br>I use [Camelot][camelot-docs]. Camelot uses PDFMiner. Camelot allows the cumbersome job of PDF processing to be largely automated. Although Camelot claim to be the [best table extraction][camelot-table-extraction-comparison] tool and it indeed is, its code is difficult to be used externally. I am hoping to use Camelot by the side of [PDFQuery].

[camelot-docs]: https://camelot-py.readthedocs.io/en/master/
[camelot-table-extraction-comparison]: https://github.com/camelot-dev/camelot/wiki/Comparison-with-other-PDF-Table-Extraction-libraries-and-tools
[PDFQuery]: https://github.com/jcushman/pdfquery

#### List of Importers

- Bank of America PDF Deposit Statement Importer
- Bank of America PDF Credit Card Statement Importer
- Chase PDF Statement Importer
- Apple iTunes Order Scraper and Importer

#### Known Issues

- Unable to recognize account number automatically.
- Unable to set the year correctly.
- Need to implement a formal way to extract / set file date.
- Need to implement a common interface.

#### Dependencies

- Camelot and its dependencies

### Venmo Importers

- Venmo CSV Importer

### [Amazon Importers](./importers/amazon/README.md)

- Amazon Retail Order History CSV Importer

### CashApp Importers

- Cash App CSV importers

## Additional Resources

- Plain text accounting [in general][plaintextaccounting-org]
- Beancount's [official documentation][official-doc] an its [unofficial take][generated-doc]
- Beancount source code on [Bitbucket][beancount-bitbucket]

[plaintextaccounting-org]: https://plaintextaccounting.org
[official-doc]: http://furius.ca/beancount/doc/index
[generated-doc]: https://xuhcc.github.io/beancount-docs/
[beancount-bitbucket]: https://bitbucket.org/blais/beancount/src
[beancount-github]: https://github.com/beancount/beancount
