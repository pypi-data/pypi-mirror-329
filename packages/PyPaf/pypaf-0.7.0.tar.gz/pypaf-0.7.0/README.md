# PyPaf

Formats the elements of a Royal Mail Postcode Address File entry according to the rules described in the [Royal Mail Programmer's Guide Edition 7, Version 6.2](https://www.poweredbypaf.com/wp-content/uploads/2024/11/Latest-Programmers_guide_Edition-7-Version-6-2.pdf)

## Installation

Install it from PyPI:

    pip install pypaf

## Usage

### Formatting

May be used to format the PAF Address elements as a list of strings:

```python
import paf
address = paf.Address({
    'building_name': "1-2",
    'thoroughfare_name': "NURSERY",
    'thoroughfare_descriptor': "LANE",
    'dependent_locality': "PENN",
    'post_town': "HIGH WYCOMBE",
    'postcode': "HP10 8LS"
})
address.as_list() # or list(address)

['1-2 NURSERY LANE', 'PENN', 'HIGH WYCOMBE', 'HP10 8LS']
```

Or as a tuple of strings:

```python
import paf
address = paf.Address({
    'building_name': "1-2",
    'thoroughfare_name': "NURSERY",
    'thoroughfare_descriptor': "LANE",
    'dependent_locality': "PENN",
    'post_town': "HIGH WYCOMBE",
    'postcode': "HP10 8LS"
})
address.as_tuple() # or tuple(address)

('1-2 NURSERY LANE', 'PENN', 'HIGH WYCOMBE', 'HP10 8LS')
```

Or as a single string:

```python
import paf
address = paf.Address({
    'building_name': "1-2",
    'thoroughfare_name': "NURSERY",
    'thoroughfare_descriptor': "LANE",
    'dependent_locality': "PENN",
    'post_town': "HIGH WYCOMBE",
    'postcode': "HP10 8LS"
})
address.as_str() # or str(address)

'1-2 NURSERY LANE, PENN, HIGH WYCOMBE. HP10 8LS'
```

Or as a dictionary:

```python
import paf
address = paf.Address({
    'building_name': "1-2",
    'thoroughfare_name': "NURSERY",
    'thoroughfare_descriptor': "LANE",
    'dependent_locality': "PENN",
    'post_town': "HIGH WYCOMBE",
    'postcode': "HP10 8LS"
})
address.as_dict()

{
    'line_1': "1-2 NURSERY LANE",
    'line_2': "PENN",
    'post_town': "HIGH WYCOMBE",
    'postcode': "HP10 8LS"
}
```

### Premises Attributes

The `sub_building_name`, `building_name` and `building_number` supplied in the source PAF Address elements need to be parsed according Programmer's Guide rules in order to correctly identify the premises elements of the address.

The Address class includes a parsed premises dictionary that contains key-values that may be used to identify the premises within the thoroughfare and the sub-premises within the premises.

The parsing decomposes the premises and sub-premises to its constituent parts:

| Key                 | Notes |
| ------------------- | ----------- |
| premises_type       | If it is of a known type e.g. BLOCK, BUILDING |
| premises_number     | Building number or leading digits of building name |
| premises_suffix     | Non-numeric characters following leading digits of building name |
| premises_name       | Building name, if it cannot be decomposed |
| sub_premises_type   | If it is of a known type e.g. FLAT, UNIT |
| sub_premises_number | Leading digits of sub-building name |
| sub_premises_suffix | Non-numeric characters following leading digits of sub-building name |
| sub_premises_name   | Sub-building name, if it cannot be decomposed |

```python
import paf
self.address = paf.Address({
    'sub_building_name': "FLAT 2B",
    'building_name': "THE TOWER",
    'building_number': "27",
    'thoroughfare_name': "JOHN",
    'thoroughfare_descriptor': "STREET",
    'post_town': "WINCHESTER",
    'postcode': "SO23 9AP"
})
address.premises()

{
    'premises_number': 27,
    'premises_name': 'THE TOWER',
    'sub_premises_type': 'FLAT',
    'sub_premises_number': 2,
    'sub_premises_suffix': 'B',
}
```

If there are no `sub_building` or `building` elements supplied the `organisation_name` or `po_box_number` elements will be used populate the premises elements, where available.

If there is no `sub_building_name` element and the `dependent_thoroughfare` elements are populated the `building` elements will be used to populate the `sub_premises` elements and the `dependent_thoroughfare` elements the `premises` elements.

```python
import paf
self.address = paf.Address({
    'building_name': "1A",
    'dependent_thoroughfare_name': "SEASTONE",
    'dependent_thoroughfare_descriptor': "COURT",
    'thoroughfare_name': "STATION",
    'thoroughfare_descriptor': "ROAD",
    'post_town': "HOLT",
    'postcode': "NR25 7HG"
})
address.premises()

{
    'premises_name': 'SEASTONE COURT',
    'sub_premises_number': 1,
    'sub_premises_suffix': 'A'
}
```

## Development

After checking out the repo, run `pytest` to run the tests.

To release a new version, update the version number in `version.py`, and then run `python -m build`, which will create a distribution archive. Run `python -m twine upload dist/*`, to upload the distribution archive to [pypi.org](https://pypi.org).

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/drabjay/pypaf. This project is intended to be a safe, welcoming space for collaboration, and contributors are expected to adhere to the [Contributor Covenant](http://contributor-covenant.org) code of conduct.

## License

The package is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).

## Code of Conduct

Everyone interacting in the PyPaf project’s codebases, issue trackers, chat rooms and mailing lists is expected to follow the [code of conduct](https://github.com/drabjayc/pypaf/blob/master/CODE_OF_CONDUCT.md).