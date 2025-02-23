===========================
Controlled Vocabulary Utils
===========================

A package for evaluating values for terms in a controlled vocabulary.

Usage
-----

.. code-block:: python

    from controlled_vocabulary_utils import Manager as ValidationManager

    config_file = "conf/controlled_vocabulary.yaml"

    vm = ValidationManager(
        config_file=config_file,
        verbose=verbose,
    )

    term = "zygosity"
    val = "mosaic"
    if vm.is_valid(term, val):
        print(f"'{val}' is a valid value for term '{term}'")
    else:
        print(f"'{val}' is NOT a valid value for term '{term}'")
