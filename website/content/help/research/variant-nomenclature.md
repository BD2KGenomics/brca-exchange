<span class="term_entry">

#### Gene ((Gene_Symbol))
The name of the gene on which the variant was found, as named by the HGNC. This will be either _BRCA1_ or _BRCA2_.

</span>

----
#### HGVS Nomenclature
A nomenclature system standardized by the Human Genome Variation Society \(HGVS\) which utilizes coordinates to name variants across genomic DNA, coding DNA, RNA, and protein molecules. Each coordinate provides an indicator of the biomolecule being referred to \('c.', 'g.', 'p.'\), a location in that biomolecule \('12345'\), and an indication of what changed in the variant \('G&gt;A', 'insA', 'dupT', 'del15', 'Asp...Asn'\). Most variant aliases utilize this standard nomenclature:
  * ##### HGVS Nucleotide ((HGVS_cDNA))
    HGVS variant alias which references the nucleotide change based on the location in the coding DNA, not the genomic DNA.
  * ##### HGVS RNA ((HGVS_RNA))
    The variant alias that uses RNA location.
  * ##### HGVS Protein ((HGVS_Protein))
    The predicted protein-level change \(if any\) that would be introduced by the genomic variant.
  * ##### Genomic Nomenclature GRCh38 ((Genomic_Coordinate_hg38))
    HGVS variant alias which references the nucleotide in genomic DNA, per the GRCh38 genome build. Click alias to access the UCSC Genome Browser.
  * ##### Genomic Nomenclature GRCh37 ((Genomic_Coordinate_hg37))
    HGVS variant alias which references the nucleotide in genomic DNA, per the GRCh37 genome build. Click alias to access the UCSC Genome Browser.
  * For more information on HGVS nomenclature, visit the [HGVS site](http://varnomen.hgvs.org/bg-material/simple/).

----

<span class="term_entry">

#### Transcript Identifier ((Reference_Sequence))
These identifiers, which typically start in ‘NM’, are gene-specific, not variant-specific. They are generally used to keep track of different transcripts submitted to databases such as RefSeq, and are carried over to ClinVar.

BRCA Exchange mainly uses two transcript identifiers. There is one main transcript used for _BRCA1_ \(NM 007294.3\) and another identifier used for _BRCA2_ \(NM 000059.3\). Other, less common transcripts are also present in the database.

</span>

----

<span class="term_entry">

#### Abbreviated AA Change ((Protein_Change))
A shortened abbreviation of the HGVS Protein alias using one-letter abbreviation for amino acids.

</span>

----

<span class="term_entry">

#### BIC designation ((BIC_Nomenclature))
A variant alias presented in BIC Nomenclature, which predates HGVS nomenclature and thus follows a different format.

</span>

----

<span class="term_entry">

#### ClinGen Allele Registry Link ((CA_ID))
Link to the variant in the ClinGen Allele Registry.

</span>

<span class="term_entry">

#### VRS Identifier ((VR_ID))
The VRS Identifier is a globally-unique identifier that removes a number of the ambiguities in variant representation. Further details are available [here](https://vr-spec.readthedocs.io/en/1.0/).

</span>
