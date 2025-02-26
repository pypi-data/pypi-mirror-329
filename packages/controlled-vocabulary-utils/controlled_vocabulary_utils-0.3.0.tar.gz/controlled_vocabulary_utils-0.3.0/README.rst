===========================
Controlled Vocabulary Utils
===========================

A package for evaluating values for terms in a controlled vocabulary.

Usage
-----


Contents of the controlled vocabulary configuration file:

.. code-block:: yaml

    ---
    format_version: 0.1.0
    name: Controlled Vocabulary for Bioinformatics
    description: TBD
    terms:
      - name: variant_effect_on_function
        def: The effect that the variant has on the function of the gene.
        datatype: string
        accepted_values:
          "loss": The variant has caused a loss of function.
          "gain": The variant has caused a gain of function.
      - name: region_of_transcript_affected
        def: The region of the transcript that the variant affects.
        datatype: string
        accepted_values:
          "start": The variant affects the start of the transcript.
          "end": The variant affects the end of the transcript.
          "whole transcript": The variant affects the whole transcript.
          "overlapping end": The variant overlaps one end of the ends of the transcript.
      - name: variant_status
        def: TBD
        alt_names:
          - variant_qc_status
        datatype: string
        accepted_values:
      - name: score
        def: TBD
        datatype: integer
        accepted_values:
          "10": "very low score"
          "20": "low score"
          "40": "mid-level score"
      - name: zygosity
        def: TBD
        alt_names:
          - zyg
        datatype: string
        accepted_values:
          "heterozygous": "heterozygous"
          "homozygous": "homozygous"
          "mosaic": "mosaic"



.. code-block:: python

    from controlled_vocabulary_utils import CVValidationManager

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
