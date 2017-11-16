#!/usr/bin/env python

'''
calcVarPriors

Parses a tsv file (default built.tsv) containing variant information and for each variant in file 
calculates either the prior probability of pathogenicity or a prior ENGIMA classification based on variant type and variant location
'''

import argparse
import csv


def checkSequence(sequence):
    '''Checks if a given sequence contains acceptable nucleotides returns True if sequence is comprised entirely of acceptable bases'''
    acceptableBases = ["A", "C", "T", "G", "N", "R", "Y"]
    badBases = 0
    if len(sequence) > 0:
        for base in sequence:
            if base not in acceptableBases:
                badBases += 1
            if badBases == 0:
                acceptableSequence = True
            else:
                # badBases > 0
                acceptableSequence = False
    else:
        # len(sequence) = 0
        acceptableSequence = False
    return acceptableSequence

def getVarStrand(variant):
    '''Given a variant, returns the coding strand based on the variant's gene_symbol'''
    varGene = variant["Gene_Symbol"]
    if varGene == "BRCA1": 
        varStrand = '-'
    elif varGene == "BRCA2":
        varStrand = '+'
    else:
        # varGene not BRCA1 or BRCA2
        varStrand = ""
    return varStrand


def getVarType(variant):
    '''
    Returns a string describing type of variant (substitution, deletion, insertion, delins, other) depending on variant reference and alternate alleles
    '''
    acceptableRefSeq = checkSequence(variant["Ref"])
    acceptableAltSeq = checkSequence(variant["Alt"])
    if acceptableRefSeq == True and acceptableAltSeq == True: 
        if len(variant["Ref"]) == len(variant["Alt"]):
            if len(variant["Ref"]) == 1:
                varType = "substitution"
            else:
                varType = "delins"
        else:
            # variant is an indel or other variant type
            if len(variant["Ref"]) > len(variant["Alt"]):
                if len(variant["Alt"]) == 1:
                    varType = "deletion"
                else:
                    # delins type variant
                    varType = "delins"
            elif len(variant["Ref"]) < len(variant["Alt"]):
                if len(variant["Ref"]) == 1:
                    varType = "insertion"
                else:
                    # delins type variant
                    varType = "delins"
            else:
                # variant is not an indel or substitution variant
                varType = "other"
    else:
        # not acceptable ref seq and alt seq, variant will not be handled by code
        varType = "other"
    return varType


def getVarLocation(variant):
    '''Given a variant, returns location of variant using Ensembl API for variant annotation'''
    # TO DO - Implement this function using Ensembl API so that variant location is identified
    varLoc = '-'
    return varLoc


def getVarDict(variant):
    '''
    Given input data, returns a dictionary containing information for each variant in input
    Dictionary key is variant HGVS_cDNA and value is a dictionary containing variant gene, variant chromosome, 
    variant strand, variant genomic coordinate, variant type, and variant location
    '''
    varHGVS = variant["pyhgvs_cDNA"]
    varGene = variant["Gene_Symbol"]
    varChrom = variant["Chr"]
    varStrand = getVarStrand(variant)
    varGenCoordinate = variant["Pos"]
    varType = getVarType(variant)
    varLoc = getVarLocation(variant)
    varDict = {"varGene":varGene,
               "varChrom":varChrom,
               "varStrand":varStrand,
               "varGenCoordinate":varGenCoordinate,
               "varType":varType,
               "varLoc":varLoc,
               "varHGVScDNA":varHGVS}
    return varDict
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', "--inputFile", default="built.tsv", help="File with variant information")
    parser.add_argument('-o', "--outputFile", help="File where results will be output")
    parser.add_arguement('-b', "--boundaries", default="ENIGMA", help="Specifies which boundaries (either ENIGMA or PRIORS) to use for clinically important domains")
    args = parser.parse_args()
    
    inputData = csv.DictReader(open(args.inputFile, "r"), delimiter="\t")
    for variant in inputData:
        varDict = getVarDict(variant)

    # TO DO - create conditional to account for user selected boundaries
    newColumns = ["varType", "varLoc", "pathProb", "ENIGMAClass", "donorVarMES", "donorVarZ", "donorRefMES", "donorRefZ", "accVarMES", "accVarZ", "accRefMES", "accRefZ", "deNovoMES", "deNovoZ", "spliceSite", "spliceRescue", "frameshift", "CNV", "spliceFlag"]
    # TO DO - create built_with_priors (copy of built) and append new columns
    
if __name__ == "__main__":
    main()