'use strict';

var React = require('react');
var PureRenderMixin = require('./PureRenderMixin'); // deep-equals version of PRM
var {Grid, Col, Row, Alert} = require('react-bootstrap');
var backend = require('./backend');

var FactSheet = React.createClass({
    mixins: [PureRenderMixin],
    getInitialState: function() {
        return {};
    },
    componentWillMount: function() {
        backend.variantCounts().subscribe(
            resp => this.setState(resp),
            () => this.setState({error: 'Problem connecting to server'}));
    },
    render: function () {
        return (
            <Grid id="main-grid" className="main-grid">
                <Row>
                    <Col md={8} mdOffset={2}>
                        <h1>BRCA Exchange: Facts & Stats</h1>
                        <br />
                        <p>Genetic variants in the BRCA1 and BRCA2 genes can reveal if a woman is predisposed to hereditary breast or ovarian cancer. While some BRCA variants have well-understood clinical significance, others require further research. The BRCA Exchange seeks to compile BRCA variation data from around the world to both facilitate this research, and to provide women and their doctors with clear information concerning their BRCA variants.</p>
                        <h3>BRCA Exchange Web Portal</h3>
                        <ul>
                            <li>The BRCA Exchange web portal is the largest public source for information on BRCA1 and BRCA2 variants.</li>
                            <li>By default, the web portal shows variants that have been expert-classified by an international panel (the ENIGMA consortium).</li>
                            <li>By switching from the ‘expert reviewed portal’ to the ‘all public data portal’, users may also explore information on variants that have not yet been classified by the expert panel. For these unclassified variants, the impact on health has not yet been established.</li>
                        </ul>
                        <u>Web portal statistics:</u>
                        {this.state.error ? <p>&nbsp;&nbsp;&nbsp;({this.state.error})</p> :
                        <ul>
                            <li>Number of unique BRCA variants in the portal: {Number(this.state.total).toLocaleString()}</li>
                            <ul>
                                <li>Unique BRCA1 variants in the portal: {Number(this.state.brca1).toLocaleString()}</li>
                                <li>Unique BRCA2 variants in the portal: {Number(this.state.brca2).toLocaleString()}</li>
                            </ul>
                            <li>Number of ENIGMA expert-classified variants in the portal: {Number(this.state.enigma).toLocaleString()}</li>
                            <ul>
                                <li>Variants expert-classified as pathogenic: {Number(this.state.enigmabrca1).toLocaleString()}</li>
                                <li>Variants expert-classified as benign: {Number(this.state.enigmabrca2).toLocaleString()}</li>
                            </ul>
                        </ul>}
                        <br />
                        <h4>Media Inquiries</h4>
                        For media inquiries, please contact the GA4GH Communications Lead, Angela Page (<a href="mailto:angela.page@genomicsandhealth.org">angela.page@genomicsandhealth.org</a>)
                        <br />
                        <br />
                        <img src={require('../content/BRCA_scaled.JPG')}></img>
                        <small><em>Source: https://commons.wikimedia.org/wiki/File:BRCA_1.JPG</em></small>

                        <h3>BRCA Genes & Cancer</h3>
                        <ul>
                            <li>The BRCA1 and BRCA2 genes typically help to prevent cancer in humans. However, when either of these genes are altered by a variation in the gene sequence, the result can be an increase in risk for hereditary breast, ovarian, or other cancers in an individual.</li>
                            <li>Not all genetic sequence variations lead to increased cancer risk. In order to better understand the impact of a BRCA variant, scientists study each variant to predict its individual impact on health.</li>
                            <li>Genetic variants may be classified as ‘pathogenic’ or ‘likely pathogenic’ (associated with greatly increased risk of disease), ‘benign’ or ‘likely benign’ (not associated with a markedly increased risk of disease), or ‘variant of unknown significance’ (impact on disease risk is unclear at this time).</li>
                            <li>Women who have a pathogenic BRCA variant are at substantially greater risk of developing cancer over their lifetime:</li>
                            <ul>
                                <li><u>Pathogenic BRCA1 variants:</u></li>
                                <ul>
                                    <li>Up to a 55% chance of developing breast cancer by age 70</li>
                                    <li>Up to a 39% cancer of developing ovarian cancer in their lifetime</li>
                                </ul>
                                <li><u>Pathogenic BRCA2 variants:</u></li>
                                <ul>
                                    <li>Up to a 45% chance of developing breast cancer by age 70</li>
                                    <li>Up to a 17% chance of developing ovarian cancer in their lifetime</li>
                                </ul>
                            </ul>
                            <li>With advances in DNA sequencing, individuals can have genetic testing performed to screen their DNA for specific known BRCA variants. Testing involves taking a blood or saliva sample from the individual. The results are interpreted by a clinical geneticist or licenced genetic counselor.</li>
                            <li>Genetic testing centres each hold a portion of the world’s knowledge about BRCA variants. By aggregating this knowledge together into one shared resource, scientists around the world can have access to greater amounts of information to assist them in classifying variants as ‘pathogenic’ or ‘benign’. This means more accurate and consistent information for doctors, patients, and families.</li>
                        </ul>
                        <Alert bsStyle="info">
                            For more information about BRCA genes and cancer, please see:
                            <ul>
                                <li><a href='http://www.cancer.gov/about-cancer/causes-prevention/genetics/brca-fact-sheet'>http://www.cancer.gov/about-cancer/causes-prevention/genetics/brca-fact-sheet</a></li>
                                <li><a href='https://seer.cancer.gov/archive/csr/1975_2011/'>SEER Cancer Statistics Review</a>, 1975-2011, National Cancer Institute. Bethesda, MD</li>
                            </ul>
                        </Alert>
                        <br />
                        <h3>The BRCA Challenge</h3>
                        <br />
                        <ul>
                            <li>The BRCA Challenge project was proposed by Professor Sir John Burn (Newcastle University, UK) at the first plenary meeting of the Global Alliance for Genomics and Health (GA4GH) in March, 2014.</li>
                            <li>In June, 2015, a meeting was held at UNESCO headquarters (Paris, France) to further develop the vision for data sharing and expert BRCA variant classification. This meeting included representation from several laboratories and organizations, including: Human Variome Project (Global Variome Ltd.), ENIGMA Consortium, Ambry Genetics, AstraZeneca, Annai Systems, ClinGen, ClinVar, Curoverse, DECIPHER, DNAnexus, ENIGMA, Genetic Alliance, Genomics England, Illumina, Inserm, Invitae, LabCorp, LOVD, New England Journal of Medicine, Quest, SolveBio, World Health Organization, and others. A major outcome of this meeting was a plan to develop a public web portal, the BRCA Exchange, to share expert-classified variants with clinicians, patients, and labs.</li>
                            <li>The project continues to be led by co-chairs John Burn and Stephen Chanock (National Cancer Institute, USA), along with a Steering Committee of international leaders in breast cancer and genomics, and in collaboration with the Human Variome Project and ENIGMA Consortium.</li>
                            <li>The goals of the BRCA Challenge are to: publicly share BRCA variants; create an environment for collaborative variant curation with access to pooled evidence; create a curated list of BRCA variants, classified by experts, to enable accurate clinical care; and address the social, ethical, and legal challenges to global data sharing alongside patient advocacy organizations worldwide.</li>
                            <li>The BRCA Exchange web portal is working to meet several of the above core goals, by publicly aggregating and sharing BRCA variants (including variants expert-classified by members of ENIGMA), and fostering a community space for collaborative variant curation.</li>
                            <li>This work reflects the combined vision of clinicians, researchers, and patient advocates from around the world. In particular, leadership has been contributed from the below individuals:</li>
                            <ul>
                                <li>John Burn, Newcastle University, Newcastle upon Tyne, UK</li>
                                <li>Stephen Chanock, National Cancer Institute, Rockville, USA</li>
                                <li>Antonis Antoniou, University of Cambridge, Cambridge, UK</li>
                                <li>Larry Brody, National Human Genome Research Institute, Bethesda, USA</li>
                                <li>Robert Cook-Deegan, Duke University, Durham, USA</li>
                                <li>Fergus Couch, Mayo Clinic, Rochester, USA</li>
                                <li>Johan den Dunnen, Leiden University Medical Center, Leiden, Netherlands</li>
                                <li>Susan Domchek, University of Pennsylvania, Philadelphia, USA</li>
                                <li>Douglas Easton, University of Cambridge, Cambridge, UK</li>
                                <li>William Foulkes, McGill University, Montreal, Canada</li>
                                <li>Judy Garber, Dana-Farber Cancer Institute, Boston, USA</li>
                                <li>David Goldgar, Huntsman Cancer Institute, Salt Lake City, USA</li>
                                <li>Kazuto Kato, Osaka University, Osaka, Japan</li>
                                <li>Delyth Jane Morgan, Baroness Morgan of Drefelin, Breast Cancer Now, Cancer Research UK</li>
                                <li>Robert Nussbaum, University of California San Francisco, San Francisco, USA</li>
                                <li>Kenneth Offit, Memorial Sloan Kettering Cancer Center, New York, USA</li>
                                <li>Sharon Plon, Baylor College of Medicine, Houston, USA</li>
                                <li>Gunnar Rätsch, ETH Zurich, Zurich, Switzerland</li>
                                <li>Nazneen Rahman, Institute of Cancer Research, London, UK</li>
                                <li>Heidi Rehm, Harvard Medical School, Boston, USA</li>
                                <li>Mark Robson, Memorial Sloan Kettering Cancer Center, New York City, USA</li>
                                <li>Wendy Rubinstein, National Institute of Health, Bethesda, USA</li>
                                <li>Amanda Spurdle, QIMR Berghofer Medical Research Institute, Herston, Australia</li>
                                <li>Dominique Stoppa-Lyonnet, Curie Institute, Paris, France</li>
                                <li>Sean Tavtigian, Hunstman Cancer Institute, Salt Lake City, USA</li>
                                <li>David Haussler, UC Santa Cruz Genomics Institute, Santa Cruz, USA</li>
                                <li>Bartha Knoppers, McGill University, Montreal, Canada</li>
                            </ul>
                        </ul>
                        <br />
                    </Col>
                    <Col md={6} mdOffset={3}>
                        <img src={require('../content/DNA_cyclepath_to_Shelford_-_geograph.org.uk_-_538440.jpg')}></img>
                        <small style={{float: 'left'}}><em>The BRCA genes loom large in public awareness. This photo shows a bicycle path in Shelford, England that depicts the sequence of the BRCA2 gene. The lanes of the path are separated by colored stripes. Each stripe represents one base of BRCA2, with the stripes color-coded according to the nucleotide. See also <a href='http://www.bshs.org.uk/travel-guide/dna-cycle-path-cambridge-england'>http://www.bshs.org.uk/travel-guide/dna-cycle-path-cambridge-england</a></em></small>
                    </Col>
                    <Col md={8} mdOffset={2}>
                        <br />
                        <Alert bsStyle='info'>
                            For more information about the BRCA Challenge and GA4GH, please visit:
                            <ul>
                                <li><a href="http://www.genomicsandhealth.org/">Global Alliance for Genomics and Health</a> (GA4GH)</li>
                                <li><a href="https://genomicsandhealth.org/work-products-demonstration-projects/brca-challenge-0">BRCA Challenge</a></li>
                            </ul>
                        </Alert>
                        <h3>Acknowledgements</h3>
    <p>
The <a href="http://brcaexchange.org">BRCA Exchange</a> website is a product of the <a href="https://genomicsandhealth.org/work-products-demonstration-projects/brca-challenge-0">BRCA Challenge</a> of the <a href="https://genomicsandhealth.org/">Global Alliance for Genomics and Health</a>. The web site and underlying database were developed by Molly Zhang, Charles Markello, Mary Goldman, Brian Craft, Zack Fischmann, Joe Thomas, David Haussler, Melissa Cline and Benedict Paten at the Computational Genomics Lab at the UC Santa Cruz Genomics Institute, Faisal Alquaddoomi and <a href="http://ratschlab.org/~raetsch">Gunnar R&auml;tsch</a> at <a href="https://www.ethz.ch/en.html">Eidgenössische Technische Hochschule Zürich</a>, and Rachel Liao of the  <a href="https://genomicsandhealth.org/">Global Alliance for Genomics and Health</a>  with input and feedback from many members of the <a href="https://genomicsandhealth.org/work-products-demonstration-projects/brca-challenge-0">BRCA Challenge</a> working groups.
</p>
<p>
Variant data on this site are made available using the standards based <a href="https://genomicsandhealth.org/work-products-demonstration-projects/genomics-api">GA4GH Genomics API</a>. For more information, and example usage please visit our <a href="/about/api">API description</a>.
</p>
<div style={{display: "inline-block", textAlign: "center" }}>
    <a href="http://genomicsandhealth.org"><img src={require('./img/ga4gh-logo-more.png')} style={{ width: 240, paddingRight: 6, paddingBottom: 8 }}></img></a>
    <a href="https://genomics.soe.ucsc.edu"><img src={require('./img/UC-Santa-Cruz-Genomics-Inst_090314.png')} style={{ width: 260, paddingBottom: 8 }}></img></a>
    <a href="https://www.ethz.ch/en.html"><img src={require('./img/ETHzurich.png')} style={{ width: 240, paddingBottom: 8 }}></img></a>
</div>
                    </Col>
                </Row>
            </Grid>
        );
    }
});

module.exports = FactSheet;
