import click
import pandas as pd


coord_col = 'genomics_coord'

VCF_INFO_COL = 7

VARS_OF_INTEREST = ["vAnnGeneAll", "BayesDel_nsfp33a_noAF"]


def _read_part(path):
    try:
        return pd.read_csv(path, sep='\t', comment='#', header=None)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def victor_results_as_df(paths):
    """
    Reading VCFs (one per chromosome) generated by the VICTOR pipeline and extracting useful information
    (e.g. bayesdel scores) out of the VCF Info field.

    :param paths: paths to VCF files annotated by VICTOR
    :return: dataframe with one column per variable of interest + join key
    """
    victor_vcf_df = pd.concat([_read_part(path) for path in paths]).reset_index(drop=True)

    # processing VCF INFO col, generate a dict variable_name -> value out of the info field for every record
    info_dict = victor_vcf_df.iloc[:, VCF_INFO_COL].str.split(';').apply(
        lambda l: {s.split('=')[0] : '='.join(s.split('=')[1:]) for s in l})

    # generating dataframe out of dict, one column per variable
    df_victor_props = pd.DataFrame.from_records(info_dict.values, index=info_dict.index)[VARS_OF_INTEREST]

    # join back to vcf dataframe
    df_ret = victor_vcf_df.merge(df_victor_props, how='inner', left_index=True, right_index=True)

    # calculate a coordinate representation to join with built_tsv
    df_ret[coord_col] = 'chr' + df_ret.iloc[:, 0].astype(str) + ":g." + df_ret.iloc[:, 1].astype(
        str) + ':' + df_ret.iloc[:, 3].astype(
        str) + ">" + df_ret.iloc[:, 4].astype(str)

    # dropping VCF columns, leaving columns for variable of interest + join field
    return df_ret.drop(columns=[c for c in range(0, VCF_INFO_COL + 1)])


@click.command()
@click.argument('vcf-parts', nargs=-1, type=click.Path(readable=True))
@click.option('--built-tsv', required=True, type=click.Path(readable=True))
@click.option('--output', required=True, type=click.Path(writable=True))
def main(vcf_parts, built_tsv, output):
    df_victor = victor_results_as_df(vcf_parts)
    df = pd.read_csv(built_tsv, sep='\t')

    df_merged = df.merge(df_victor, left_on='Genomic_Coordinate_hg38', right_on=coord_col, how='left')

    # drop join key and write
    (df_merged.drop(columns=[coord_col]).
     to_csv(output, sep='\t', index=False))


if __name__ == "__main__":
    main()
