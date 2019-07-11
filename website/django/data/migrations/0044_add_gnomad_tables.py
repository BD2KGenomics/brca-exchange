# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-07-10 19:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0043_variantrepresentation'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportGnomadData',
            fields=[
                ('Report', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='data.Report')),
                ('Flags_GnomAD', models.TextField()),
                ('Consequence_GnomAD', models.TextField()),
                ('Variant_id_GnomAD', models.TextField()),
                ('Allele_count_genome_AFR_GnomAD', models.TextField()),
                ('Allele_count_hemi_genome_AFR_GnomAD', models.TextField()),
                ('Allele_count_hom_genome_AFR_GnomAD', models.TextField()),
                ('Allele_number_genome_AFR_GnomAD', models.TextField()),
                ('Allele_frequency_genome_AFR_GnomAD', models.TextField()),
                ('Allele_count_genome_AMR_GnomAD', models.TextField()),
                ('Allele_count_hemi_genome_AMR_GnomAD', models.TextField()),
                ('Allele_count_hom_genome_AMR_GnomAD', models.TextField()),
                ('Allele_number_genome_AMR_GnomAD', models.TextField()),
                ('Allele_frequency_genome_AMR_GnomAD', models.TextField()),
                ('Allele_count_genome_ASJ_GnomAD', models.TextField()),
                ('Allele_count_hemi_genome_ASJ_GnomAD', models.TextField()),
                ('Allele_count_hom_genome_ASJ_GnomAD', models.TextField()),
                ('Allele_number_genome_ASJ_GnomAD', models.TextField()),
                ('Allele_frequency_genome_ASJ_GnomAD', models.TextField()),
                ('Allele_count_genome_EAS_GnomAD', models.TextField()),
                ('Allele_count_hemi_genome_EAS_GnomAD', models.TextField()),
                ('Allele_count_hom_genome_EAS_GnomAD', models.TextField()),
                ('Allele_number_genome_EAS_GnomAD', models.TextField()),
                ('Allele_frequency_genome_EAS_GnomAD', models.TextField()),
                ('Allele_count_genome_FIN_GnomAD', models.TextField()),
                ('Allele_count_hemi_genome_FIN_GnomAD', models.TextField()),
                ('Allele_count_hom_genome_FIN_GnomAD', models.TextField()),
                ('Allele_number_genome_FIN_GnomAD', models.TextField()),
                ('Allele_frequency_genome_FIN_GnomAD', models.TextField()),
                ('Allele_count_genome_NFE_GnomAD', models.TextField()),
                ('Allele_count_hemi_genome_NFE_GnomAD', models.TextField()),
                ('Allele_count_hom_genome_NFE_GnomAD', models.TextField()),
                ('Allele_number_genome_NFE_GnomAD', models.TextField()),
                ('Allele_frequency_genome_NFE_GnomAD', models.TextField()),
                ('Allele_count_genome_OTH_GnomAD', models.TextField()),
                ('Allele_count_hemi_genome_OTH_GnomAD', models.TextField()),
                ('Allele_count_hom_genome_OTH_GnomAD', models.TextField()),
                ('Allele_number_genome_OTH_GnomAD', models.TextField()),
                ('Allele_frequency_genome_OTH_GnomAD', models.TextField()),
                ('Allele_count_genome_SAS_GnomAD', models.TextField()),
                ('Allele_count_hemi_genome_SAS_GnomAD', models.TextField()),
                ('Allele_count_hom_genome_SAS_GnomAD', models.TextField()),
                ('Allele_number_genome_SAS_GnomAD', models.TextField()),
                ('Allele_frequency_genome_SAS_GnomAD', models.TextField()),
                ('Allele_count_genome_GnomAD', models.TextField()),
                ('Allele_number_genome_GnomAD', models.TextField()),
                ('Allele_frequency_genome_GnomAD', models.TextField()),
                ('Allele_count_exome_AFR_GnomAD', models.TextField()),
                ('Allele_count_hom_exome_AFR_GnomAD', models.TextField()),
                ('Allele_number_exome_AFR_GnomAD', models.TextField()),
                ('Allele_frequency_exome_AFR_GnomAD', models.TextField()),
                ('Allele_count_exome_AMR_GnomAD', models.TextField()),
                ('Allele_count_hemi_exome_AMR_GnomAD', models.TextField()),
                ('Allele_count_hom_exome_AMR_GnomAD', models.TextField()),
                ('Allele_number_exome_AMR_GnomAD', models.TextField()),
                ('Allele_frequency_exome_AMR_GnomAD', models.TextField()),
                ('Allele_count_exome_ASJ_GnomAD', models.TextField()),
                ('Allele_count_hemi_exome_ASJ_GnomAD', models.TextField()),
                ('Allele_count_hom_exome_ASJ_GnomAD', models.TextField()),
                ('Allele_number_exome_ASJ_GnomAD', models.TextField()),
                ('Allele_frequency_exome_ASJ_GnomAD', models.TextField()),
                ('Allele_count_exome_EAS_GnomAD', models.TextField()),
                ('Allele_count_hemi_exome_EAS_GnomAD', models.TextField()),
                ('Allele_count_hom_exome_EAS_GnomAD', models.TextField()),
                ('Allele_number_exome_EAS_GnomAD', models.TextField()),
                ('Allele_frequency_exome_EAS_GnomAD', models.TextField()),
                ('Allele_count_exome_FIN_GnomAD', models.TextField()),
                ('Allele_count_hemi_exome_FIN_GnomAD', models.TextField()),
                ('Allele_count_hom_exome_FIN_GnomAD', models.TextField()),
                ('Allele_number_exome_FIN_GnomAD', models.TextField()),
                ('Allele_frequency_exome_FIN_GnomAD', models.TextField()),
                ('Allele_count_exome_NFE_GnomAD', models.TextField()),
                ('Allele_count_hemi_exome_NFE_GnomAD', models.TextField()),
                ('Allele_count_hom_exome_NFE_GnomAD', models.TextField()),
                ('Allele_number_exome_NFE_GnomAD', models.TextField()),
                ('Allele_frequency_exome_NFE_GnomAD', models.TextField()),
                ('Allele_count_exome_OTH_GnomAD', models.TextField()),
                ('Allele_count_hemi_exome_OTH_GnomAD', models.TextField()),
                ('Allele_count_hom_exome_OTH_GnomAD', models.TextField()),
                ('Allele_number_exome_OTH_GnomAD', models.TextField()),
                ('Allele_frequency_exome_OTH_GnomAD', models.TextField()),
                ('Allele_count_exome_SAS_GnomAD', models.TextField()),
                ('Allele_count_hemi_exome_SAS_GnomAD', models.TextField()),
                ('Allele_count_hom_exome_SAS_GnomAD', models.TextField()),
                ('Allele_number_exome_SAS_GnomAD', models.TextField()),
                ('Allele_frequency_exome_SAS_GnomAD', models.TextField()),
                ('Allele_number_exome_GnomAD', models.TextField()),
                ('Allele_count_exome_GnomAD', models.TextField()),
                ('Allele_frequency_exome_GnomAD', models.TextField()),
                ('Allele_count_hom_ASJ_GnomAD', models.TextField()),
                ('Allele_number_NFE_GnomAD', models.TextField()),
                ('Allele_number_OTH_GnomAD', models.TextField()),
                ('Allele_count_hemi_FIN_GnomAD', models.TextField()),
                ('Allele_count_hom_AMR_GnomAD', models.TextField()),
                ('Allele_count_hemi_AFR_GnomAD', models.TextField()),
                ('Allele_frequency_FIN_GnomAD', models.TextField()),
                ('Allele_count_hemi_NFE_GnomAD', models.TextField()),
                ('Allele_count_hom_NFE_GnomAD', models.TextField()),
                ('Allele_frequency_ASJ_GnomAD', models.TextField()),
                ('Allele_frequency_EAS_GnomAD', models.TextField()),
                ('Allele_frequency_AMR_GnomAD', models.TextField()),
                ('Allele_count_hemi_SAS_GnomAD', models.TextField()),
                ('Allele_count_hom_EAS_GnomAD', models.TextField()),
                ('Allele_number_ASJ_GnomAD', models.TextField()),
                ('Allele_number_FIN_GnomAD', models.TextField()),
                ('Allele_count_hom_AFR_GnomAD', models.TextField()),
                ('Allele_count_hemi_AMR_GnomAD', models.TextField()),
                ('Allele_frequency_AFR_GnomAD', models.TextField()),
                ('Allele_count_hom_OTH_GnomAD', models.TextField()),
                ('Allele_frequency_OTH_GnomAD', models.TextField()),
                ('Allele_count_hom_FIN_GnomAD', models.TextField()),
                ('Allele_count_hemi_EAS_GnomAD', models.TextField()),
                ('Allele_number_AFR_GnomAD', models.TextField()),
                ('Allele_count_hemi_OTH_GnomAD', models.TextField()),
                ('Allele_count_hom_SAS_GnomAD', models.TextField()),
                ('Allele_frequency_NFE_GnomAD', models.TextField()),
                ('Allele_number_EAS_GnomAD', models.TextField()),
                ('Allele_number_SAS_GnomAD', models.TextField()),
                ('Allele_count_hemi_ASJ_GnomAD', models.TextField()),
                ('Allele_frequency_SAS_GnomAD', models.TextField()),
                ('Allele_number_AMR_GnomAD', models.TextField()),
            ],
            options={
                'db_table': 'reportgnomaddata',
            },
        ),
        migrations.CreateModel(
            name='VariantGnomadData',
            fields=[
                ('Variant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='data.Variant')),
                ('Flags_GnomAD', models.TextField()),
                ('Consequence_GnomAD', models.TextField()),
                ('Variant_id_GnomAD', models.TextField()),
                ('Allele_count_genome_AFR_GnomAD', models.TextField()),
                ('Allele_count_hemi_genome_AFR_GnomAD', models.TextField()),
                ('Allele_count_hom_genome_AFR_GnomAD', models.TextField()),
                ('Allele_number_genome_AFR_GnomAD', models.TextField()),
                ('Allele_frequency_genome_AFR_GnomAD', models.TextField()),
                ('Allele_count_genome_AMR_GnomAD', models.TextField()),
                ('Allele_count_hemi_genome_AMR_GnomAD', models.TextField()),
                ('Allele_count_hom_genome_AMR_GnomAD', models.TextField()),
                ('Allele_number_genome_AMR_GnomAD', models.TextField()),
                ('Allele_frequency_genome_AMR_GnomAD', models.TextField()),
                ('Allele_count_genome_ASJ_GnomAD', models.TextField()),
                ('Allele_count_hemi_genome_ASJ_GnomAD', models.TextField()),
                ('Allele_count_hom_genome_ASJ_GnomAD', models.TextField()),
                ('Allele_number_genome_ASJ_GnomAD', models.TextField()),
                ('Allele_frequency_genome_ASJ_GnomAD', models.TextField()),
                ('Allele_count_genome_EAS_GnomAD', models.TextField()),
                ('Allele_count_hemi_genome_EAS_GnomAD', models.TextField()),
                ('Allele_count_hom_genome_EAS_GnomAD', models.TextField()),
                ('Allele_number_genome_EAS_GnomAD', models.TextField()),
                ('Allele_frequency_genome_EAS_GnomAD', models.TextField()),
                ('Allele_count_genome_FIN_GnomAD', models.TextField()),
                ('Allele_count_hemi_genome_FIN_GnomAD', models.TextField()),
                ('Allele_count_hom_genome_FIN_GnomAD', models.TextField()),
                ('Allele_number_genome_FIN_GnomAD', models.TextField()),
                ('Allele_frequency_genome_FIN_GnomAD', models.TextField()),
                ('Allele_count_genome_NFE_GnomAD', models.TextField()),
                ('Allele_count_hemi_genome_NFE_GnomAD', models.TextField()),
                ('Allele_count_hom_genome_NFE_GnomAD', models.TextField()),
                ('Allele_number_genome_NFE_GnomAD', models.TextField()),
                ('Allele_frequency_genome_NFE_GnomAD', models.TextField()),
                ('Allele_count_genome_OTH_GnomAD', models.TextField()),
                ('Allele_count_hemi_genome_OTH_GnomAD', models.TextField()),
                ('Allele_count_hom_genome_OTH_GnomAD', models.TextField()),
                ('Allele_number_genome_OTH_GnomAD', models.TextField()),
                ('Allele_frequency_genome_OTH_GnomAD', models.TextField()),
                ('Allele_count_genome_SAS_GnomAD', models.TextField()),
                ('Allele_count_hemi_genome_SAS_GnomAD', models.TextField()),
                ('Allele_count_hom_genome_SAS_GnomAD', models.TextField()),
                ('Allele_number_genome_SAS_GnomAD', models.TextField()),
                ('Allele_frequency_genome_SAS_GnomAD', models.TextField()),
                ('Allele_count_genome_GnomAD', models.TextField()),
                ('Allele_number_genome_GnomAD', models.TextField()),
                ('Allele_frequency_genome_GnomAD', models.TextField()),
                ('Allele_count_exome_AFR_GnomAD', models.TextField()),
                ('Allele_count_hom_exome_AFR_GnomAD', models.TextField()),
                ('Allele_number_exome_AFR_GnomAD', models.TextField()),
                ('Allele_frequency_exome_AFR_GnomAD', models.TextField()),
                ('Allele_count_exome_AMR_GnomAD', models.TextField()),
                ('Allele_count_hemi_exome_AMR_GnomAD', models.TextField()),
                ('Allele_count_hom_exome_AMR_GnomAD', models.TextField()),
                ('Allele_number_exome_AMR_GnomAD', models.TextField()),
                ('Allele_frequency_exome_AMR_GnomAD', models.TextField()),
                ('Allele_count_exome_ASJ_GnomAD', models.TextField()),
                ('Allele_count_hemi_exome_ASJ_GnomAD', models.TextField()),
                ('Allele_count_hom_exome_ASJ_GnomAD', models.TextField()),
                ('Allele_number_exome_ASJ_GnomAD', models.TextField()),
                ('Allele_frequency_exome_ASJ_GnomAD', models.TextField()),
                ('Allele_count_exome_EAS_GnomAD', models.TextField()),
                ('Allele_count_hemi_exome_EAS_GnomAD', models.TextField()),
                ('Allele_count_hom_exome_EAS_GnomAD', models.TextField()),
                ('Allele_number_exome_EAS_GnomAD', models.TextField()),
                ('Allele_frequency_exome_EAS_GnomAD', models.TextField()),
                ('Allele_count_exome_FIN_GnomAD', models.TextField()),
                ('Allele_count_hemi_exome_FIN_GnomAD', models.TextField()),
                ('Allele_count_hom_exome_FIN_GnomAD', models.TextField()),
                ('Allele_number_exome_FIN_GnomAD', models.TextField()),
                ('Allele_frequency_exome_FIN_GnomAD', models.TextField()),
                ('Allele_count_exome_NFE_GnomAD', models.TextField()),
                ('Allele_count_hemi_exome_NFE_GnomAD', models.TextField()),
                ('Allele_count_hom_exome_NFE_GnomAD', models.TextField()),
                ('Allele_number_exome_NFE_GnomAD', models.TextField()),
                ('Allele_frequency_exome_NFE_GnomAD', models.TextField()),
                ('Allele_count_exome_OTH_GnomAD', models.TextField()),
                ('Allele_count_hemi_exome_OTH_GnomAD', models.TextField()),
                ('Allele_count_hom_exome_OTH_GnomAD', models.TextField()),
                ('Allele_number_exome_OTH_GnomAD', models.TextField()),
                ('Allele_frequency_exome_OTH_GnomAD', models.TextField()),
                ('Allele_count_exome_SAS_GnomAD', models.TextField()),
                ('Allele_count_hemi_exome_SAS_GnomAD', models.TextField()),
                ('Allele_count_hom_exome_SAS_GnomAD', models.TextField()),
                ('Allele_number_exome_SAS_GnomAD', models.TextField()),
                ('Allele_frequency_exome_SAS_GnomAD', models.TextField()),
                ('Allele_number_exome_GnomAD', models.TextField()),
                ('Allele_count_exome_GnomAD', models.TextField()),
                ('Allele_frequency_exome_GnomAD', models.TextField()),
                ('Allele_count_hom_ASJ_GnomAD', models.TextField()),
                ('Allele_number_NFE_GnomAD', models.TextField()),
                ('Allele_number_OTH_GnomAD', models.TextField()),
                ('Allele_count_hemi_FIN_GnomAD', models.TextField()),
                ('Allele_count_hom_AMR_GnomAD', models.TextField()),
                ('Allele_count_hemi_AFR_GnomAD', models.TextField()),
                ('Allele_frequency_FIN_GnomAD', models.TextField()),
                ('Allele_count_hemi_NFE_GnomAD', models.TextField()),
                ('Allele_count_hom_NFE_GnomAD', models.TextField()),
                ('Allele_frequency_ASJ_GnomAD', models.TextField()),
                ('Allele_frequency_EAS_GnomAD', models.TextField()),
                ('Allele_frequency_AMR_GnomAD', models.TextField()),
                ('Allele_count_hemi_SAS_GnomAD', models.TextField()),
                ('Allele_count_hom_EAS_GnomAD', models.TextField()),
                ('Allele_number_ASJ_GnomAD', models.TextField()),
                ('Allele_number_FIN_GnomAD', models.TextField()),
                ('Allele_count_hom_AFR_GnomAD', models.TextField()),
                ('Allele_count_hemi_AMR_GnomAD', models.TextField()),
                ('Allele_frequency_AFR_GnomAD', models.TextField()),
                ('Allele_count_hom_OTH_GnomAD', models.TextField()),
                ('Allele_frequency_OTH_GnomAD', models.TextField()),
                ('Allele_count_hom_FIN_GnomAD', models.TextField()),
                ('Allele_count_hemi_EAS_GnomAD', models.TextField()),
                ('Allele_number_AFR_GnomAD', models.TextField()),
                ('Allele_count_hemi_OTH_GnomAD', models.TextField()),
                ('Allele_count_hom_SAS_GnomAD', models.TextField()),
                ('Allele_frequency_NFE_GnomAD', models.TextField()),
                ('Allele_number_EAS_GnomAD', models.TextField()),
                ('Allele_number_SAS_GnomAD', models.TextField()),
                ('Allele_count_hemi_ASJ_GnomAD', models.TextField()),
                ('Allele_frequency_SAS_GnomAD', models.TextField()),
                ('Allele_number_AMR_GnomAD', models.TextField()),
            ],
            options={
                'db_table': 'variantgnomaddata',
            },
        ),
        migrations.AddField(
            model_name='report',
            name='BX_ID_GnomAD',
            field=models.TextField(default=b''),
        ),
        migrations.AddField(
            model_name='variant',
            name='BX_ID_GnomAD',
            field=models.TextField(default=b''),
        ),
        migrations.RunSQL(
            """
            DROP MATERIALIZED VIEW IF EXISTS currentvariant;
            CREATE MATERIALIZED VIEW currentvariant AS (
                SELECT * FROM "variant" WHERE (
                    "id" IN ( SELECT DISTINCT ON ("Genomic_Coordinate_hg38") "id" FROM "variant" ORDER BY "Genomic_Coordinate_hg38" ASC, "Data_Release_id" DESC )
                )
            );
            """
        ),
    ]
