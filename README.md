# csvu

**csvu** empowers CSV files with units, encoding them into the one-line header.

## Prior art

Originally inspired by [Read data from csv](https://pint-pandas.readthedocs.io/en/latest/user/reading.html#read-data-from-csv) in the admirable `pint-pandas`, except that that requires a second line of header for the units, which is impossible in

- [Confluence databases](https://www.atlassian.com/software/confluence/databases) or
- [Microsoft Lists](https://www.microsoft.com/en-us/microsoft-365/microsoft-lists)

They only permit a single-line header.

See also: [Parsing CSV with units in the header hgrecco/pint-pandas#166](https://github.com/hgrecco/pint-pandas/issues/166), an issue raised almost two years ago, 2023-04-09, at the launching of this project.
