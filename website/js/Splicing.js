'use strict';

var React = require('react'),
    _ = require('lodash'),
    brca1Exons = JSON.parse(require('raw!../content/brca1LollipopDomain.json')),
    brca2Exons = JSON.parse(require('raw!../content/brca2LollipopDomain.json'));

const intronWidth = 40,
    exonFill = "#c1ddf0",
    exonStroke = "rgba(0, 0, 0, 0.5)",
    exonBorderRadius = 4,
    intronFill = "#dfe6ec",
    intronStroke = "rgba(0, 0, 0, 0.5)",
    highlightFill = "#ffffbb",
    highlightStroke = "rgba(0, 0, 0, 0.5)",
    // made up values, how do I get UTR sizes for BRCA1 and BRCA2?
    leaderSize = 75,
    tailSize = 50,
    zoomMargin = 200;

function exonSizeTx (bases) {
    return bases > 150 ? 150 + Math.sqrt(bases - 150) : bases;
}

function variantInfo (variant) {
    let [before, after] = _.map(variant.Genomic_Coordinate_hg38.split(':').pop().split('>'), e => e.length);
    if (before === 1 && after === 1) {
        return { changed: 1 };
    }
    before--; after--; // since CG>G is a removal of one base, not a removal of two and insertion of one
    return {
        changed: Math.min(before, after),
        inserted: after > before ? after - before : 0,
        deleted: before > after ? before - after : 0
    };
}

// given the intervals (a: [a1, a2], b: [b1, b2]), return true if the two overlap (inclusive)
function overlaps(a, b) {
    // ensure the pairs are internally sorted
    const as = (a[0] <= a[1]) ? a : [a[1], a[0]];
    const bs = (b[0] <= b[1]) ? b : [b[1], b[0]];
    // sort each pair to reduce the number of cases we need to check
    const [first, second] = (as[0] < bs[0]) ? [as, bs] : [bs, as];

    // they can only overlap if first extends into (including surpassing) second
    return first[1] >= second[0];
}

function variantInExon (variant, exon) {
    return overlaps([variant.Hg38_Start, variant.Hg38_End], exon);
}

function variantInIntron (variant, exon, followingExon) {
    // TODO: determine how to handle intersection (where exon ends and intron starts)
    // ^ the semantics of this function have changed to just returning whether the intron overlaps the variant,
    // ^ possibly fixing the above in a roundabout way
    // Intron runs from end of one exon to beginning of next exon
    let intron = [exon[1] + 1, followingExon[0] - 1];

    return overlaps([variant.Hg38_Start, variant.Hg38_End], intron);
}
    }
};

class Variant extends React.Component {
    constructor(props) {
        super(props);
    }
    render() {
        let { variant,
              x,
              width,
              height,
              txStart,
              txEnd } = this.props;

        let variantStart, variantX, variantChange, variantChangedWidth, variantDeletedWidth, variantInsertedWidth;
        // txStart, txEnd are the parent exon/intron's span in bases
        // width, height is the pixel width, height of the parent element
        // x is the pixel position of the parent exon/intron in the SVG

        variantStart = variant.Hg38_Start;
        variantX = x + width * (variantStart - txStart) / (txEnd - txStart);

        variantChange = variantInfo(variant);

        variantChangedWidth = variantChange.changed ? width * variantChange.changed / (txEnd - txStart) : 0;
        variantDeletedWidth = variantChange.deleted ? width * variantChange.deleted / (txEnd - txStart) : 0;
        variantInsertedWidth = variantChange.inserted ? width * variantChange.inserted / (txEnd - txStart) : 0;

        // Don't show less than 2 for a variant's width
        variantChangedWidth = variantChangedWidth && Math.max(2, variantChangedWidth);
        variantDeletedWidth = variantDeletedWidth && Math.max(2, variantDeletedWidth);
        variantInsertedWidth = variantInsertedWidth && Math.max(2, variantInsertedWidth);
        // variantStart is the start of this variant in bases
        // variantX is the pixel position of this variant (assumedly) within the parent exon/intron
        // (if variantX is negative, it's because the variant's start is before this region begins)

        // Variant may cross exon/intron boundaries, so the element's maximum size can only be that of
        // its containing exon/intron
        variantChangedWidth = Math.min(variantChangedWidth, width);
        variantDeletedWidth = Math.min(variantDeletedWidth, width);
        variantInsertedWidth = Math.min(variantInsertedWidth, width);

        if (variantX - x + variantChangedWidth + variantDeletedWidth + variantInsertedWidth > width) {
            variantX = x + width - variantChangedWidth - variantDeletedWidth - variantInsertedWidth;
        }

        return (
            <g>
                <rect x={variantX} width={variantChangedWidth} height={height} fill="lightgreen" />
                <rect x={variantX + variantChangedWidth} width={variantDeletedWidth} height={height} fill="url(#diagonalHatch)" />
                <rect x={variantX + variantChangedWidth} width={variantInsertedWidth} height={height} fill="lightblue" />
            </g>
        );
    }
}

class Exon extends React.Component {
    constructor(props) {
        super(props);
    }
    componendDidMount() {
    }
    render() {
        let { n,
              txStart,
              txEnd,
              width,
              height,
              x,
              variant,
              highlight
        } = this.props;

        return (
            <g>
                <rect x={x} width={width} height={height} rx={4} ry={4} fill={highlight ? highlightFill : exonFill} stroke={highlight ? highlightStroke : exonStroke} />
                <text x={x + width / 2} y={height + 14} textAnchor="middle">{n}</text>
                { variant &&
                    <Variant variant={variant} x={x} width={width} height={height} txStart={txStart} txEnd={txEnd} /> }
            </g>
        );
    }
}

class Intron extends React.Component {
    render() {
        let { txStart,
              txEnd,
              x,
              height,
              width,
              variant,
              highlight
        } = this.props;

        return (
            <g transform="translate(0, 10)">
                <rect x={x} width={width} height={height} fill={highlight ? highlightFill : intronFill} stroke={highlight ? highlightStroke : intronStroke} />
                { variant !== undefined &&
                    <Variant variant={variant} x={x} width={width} height={height} txStart={txStart} txEnd={txEnd} /> }
            </g>
        );
    }
}

class Transcript extends React.Component {
    render() {
        let { variant,
              exons,
              preceding,
              following,
              width
        } = this.props;

        let scale,
            blocks = [],
            x,
            zoomLineStartLeft,
            zoomLineStartRight;

        preceding = Math.max(preceding, 0);
        following = Math.min(following, exons.length - 1);

        // precalculate scale
        // TODO: scales are slightly different between exonic / intronic variants. fix.
        {
            let totalWidth = 0;
            for (let i = 0; i < exons.length; i++) {
                totalWidth += exonSizeTx(exons[i][1] - exons[i][0]);
                if (i < exons.length - 1) {
                    totalWidth += intronWidth;
                }
            }
            totalWidth += leaderSize + tailSize;
            // variant is intronic
            if (following - preceding === 1) {
                totalWidth += intronWidth;
            }
            scale = (this.props.width - 2) / totalWidth;
        }

        x = leaderSize * scale;

        for (let i = 0; i < exons.length; i++) {
            let exon = exons[i];
            let exonWidth = scale * exonSizeTx(exon[1] - exon[0]);

            // draw exon
            {
                let highlight, _variant;
                if (i >= preceding && i <= following) { // exon is adjacent to, or contains, variant
                    highlight = true;
                    console.log(variant.Hg38_Start, variant.Hg38_End, exon);
                    if (variantInExon(variant, exon)) {
                        _variant = variant;
                    }
                }
                blocks.push(<Exon n={i + 1} x={x} width={exonWidth} height={40} txStart={exon[0]} txEnd={exon[1]} highlight={highlight} variant={_variant} />);
            }

            if (i === preceding) {
                zoomLineStartLeft = x;
            } else if (i === following) {
                zoomLineStartRight = x + exonWidth;
            }

            x += exonWidth;

            // draw intron
            if (i < exons.length - 1) {
                let highlight, _variant;
                if (i >= preceding && i < following) {  // intron is adjacent to, or contains, variant
                    highlight = true;
                    if (variantInIntron(variant, exon, exons[i + 1])) {
                        _variant = variant;
                    }
                }
                blocks.push(<Intron txStart={exon[1]} txEnd={exons[i + 1][0]} x={x} width={scale * intronWidth} height={20} highlight={highlight} variant={_variant} />);
                x += scale * intronWidth;
            }
        }
        return (
            <g>
                <line x1={zoomLineStartLeft} y1={50} x2={zoomMargin} y2={95} stroke="#ccc" strokeWidth="3" strokeDasharray="8,3" fill="none" />
                <line x1={zoomLineStartRight} y1={50} x2={width - zoomMargin - 2.5} y2={95} stroke="#ccc" strokeWidth="3" strokeDasharray="8,3" fill="none" />
                <rect x={0} y={53} width={820} height={14} fill="rgba(255,255,255,0.6" />
                <g transform="translate(0, 10)">
                    <rect x={1} y={8} width={scale * leaderSize} height={24} fill={intronFill} stroke={intronStroke} />
                    { blocks }
                    <rect x={x} y={8} width={scale * tailSize} height={24} fill={intronFill} stroke={intronStroke} />
                </g>
            </g>
        );
    }
}

class Zoom extends React.Component {
    render() {
        let { variant,
              exons,
              preceding,
              following,
              width
        } = this.props;

        let blocks = [],
            scale,
            x = zoomMargin;

        preceding = Math.max(preceding, 0);
        following = Math.min(following, exons.length - 1);

        // precalculate scale
        {
            let totalWidth = 0;
            for (let i = preceding; i <= following; i++) {
                totalWidth += exonSizeTx(exons[i][1] - exons[i][0]);
                if (i <= following - 1) {
                    totalWidth += intronWidth;
                    // variant is intronic
                    if (following - preceding === 1) {
                        totalWidth += intronWidth;
                    }
                }
            }
            scale = (width - 2 * zoomMargin) / totalWidth;
        }

        for (let i = preceding; i <= following; i++) {
            let exon = exons[i],
                exonWidth = scale * exonSizeTx(exon[1] - exon[0]);

            {
                let _variant;
                if (variantInExon(variant, exon)) {
                    _variant = variant;
                }
                blocks.push(<Exon n={i + 1} txStart={exon[0]} txEnd={exon[1]} x={x} width={exonWidth} height={80} highlight={true} variant={_variant} />);
            }

            x += exonWidth;
            if (i !== following) {
                let _variant, _intronWidth = intronWidth;
                if (variantInIntron(variant, exon, exons[i + 1])) {
                    _variant = variant;
                }
                if (following - preceding === 1) {
                    _intronWidth *= 2;
                }
                blocks.push(<Intron txStart={exon[1]} txEnd={exons[i + 1][0]} x={x} width={scale * _intronWidth} height={60} highlight={true} variant={_variant} />);
                x += scale * _intronWidth;
            }
        }
        return (
            <g transform="translate(0, 100)">
                { blocks }
            </g>
        );
    }
}

class Splicing extends React.Component {
    componentDidMount() {
    }
    componentWillUnmount() {
    }
    render() {
        let { variant } = this.props;

        let width = 800,
            info = variantInfo(variant),
            variantStart = variant.Hg38_Start,
            variantEnd = variant.Hg38_End,
            exons = _.map(variant.Gene_Symbol === "BRCA1" ? brca1Exons : brca2Exons, e => e.coord.split('-')),
            precedingExonIndex, followingExonIndex;

        if (variantStart < exons[0][0] || variantEnd > exons[exons.length - 1][1]) {
            return (
                <h4 style={{textAlign: 'center'}}>Variant is outside of transcript.</h4>
            );
        }

        for (let i = 0; i < exons.length; i++) {
            if (exons[i][0] > variantStart && precedingExonIndex === undefined) {
                if (exons[i - 1][1] < variantStart) {
                    precedingExonIndex = i - 1;
                } else {
                    precedingExonIndex = i - 2;
                }
            }
            if (exons[i][0] > variantEnd && followingExonIndex === undefined) {
                    followingExonIndex = i;
            }
        }

        let plural = n => n === 1 ? '' : 's';
        return (
        <div>
            <svg viewBox="-4 0 808 240" preserveAspectRatio="true">
                <pattern id="diagonalHatch" patternUnits="userSpaceOnUse" width="4" height="4">
                  <rect x="0" y="0" width="4" height="4" fill="#FF8888" />
                  <path d="M-1,1 l2,-2
                           M0,4 l4,-4
                           M3,5 l2,-2"
                        stroke="black" strokeWidth={1} />
                </pattern>
                <Transcript variant={variant} exons={exons} preceding={precedingExonIndex} following={followingExonIndex} width={width} />
                <Zoom variant={variant} exons={exons} preceding={precedingExonIndex} following={followingExonIndex} width={width} />
                <g transform="translate(274,220)">
                    <rect x="0" fill="lightgreen" stroke="black" width="20" height="10" />
                    <text x="22" y="10">{ `Substitution (${info.changed} base${plural(info.changed)})` }</text>
                    <rect x="192" fill="url(#diagonalHatch)" stroke="black" width="20" height="10" />
                    <text x="214" y="10">{ `Deletion (${info.deleted || 0} base${plural(info.deleted)})` }</text>
                    <rect x="360" fill="#56F" stroke="black" width="20" height="10"/>
                    <text x="382" y="10">{ `Insertion (${info.inserted || 0} base${plural(info.inserted)})` }</text>
                </g>
            </svg>
        </div>
        );
    }
}

module.exports = Splicing;