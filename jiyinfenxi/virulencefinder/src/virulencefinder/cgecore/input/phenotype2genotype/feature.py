#!/usr/bin/env python3

from signal import *
# import urllib.parse



class Feature(object):
    """ A feature describes a location on a genome/contig.
        The 'type' variable should be used to describe the type of feature. For
        example 'gene', 'promoter' etc. It is suggested that features that only
        describes a part of a gene, promoter etc. is prefixed with "partial_"
        (e.g. 'partial_gene'). It is also suggested that features describing a
        part of the genome without anotations/function is named 'region'.
    """
    def __init__(self, unique_id, seq_region=None, start=None, hit=None,
                 isolate=None, ref_db=None):
        self.id = unique_id
        self.unique_id = unique_id
        self.seq_region = Feature.na2none(seq_region)
        start = Feature.na2none(start)
        if(start):
            self.start = int(start)
        else:
            self.start = None
        self.hit = Feature.na2none(hit)
        self.isolate = Feature.na2none(isolate)
        self.ref_db = Feature.na2none(ref_db)

    @staticmethod
    def na2none(entry):
        if(isinstance(entry, str)):
            if(entry.upper() == "NA"):
                return None
        return entry

    def __eq__(self, other):
        if isinstance(other, Feature):
            return other.unique_id == self.unique_id
        elif isinstance(other, str):
            return other == self.unique_id
        else:
            return NotImplemented

    def __hash__(self):
        return hash(self.unique_id)


class Resistance(object):
    """ Proposal for resistance class"""
    def __init__(self, ab_class=None, pmids=None, notes=None):
        self.ab_class = Feature.na2none(ab_class)
        self.pmids = Feature.na2none(pmids)
        self.notes = Feature.na2none(notes)


class Gene(Feature):
    """
    """
    def __init__(self, unique_id, seq_region=None, start=None, end=None,
                 hit=None, isolate=None, pmids=None, notes=None, ref_db=None):
        Feature.__init__(self, unique_id=unique_id, seq_region=seq_region,
                         start=start, hit=hit, isolate=isolate, ref_db=ref_db)
        end = Feature.na2none(end)
        if(end):
            self.end = int(end)
        else:
            self.end = None


class ResGene(Gene, Resistance):
    """
    """
    def __init__(self, unique_id, seq_region=None, start=None, end=None,
                 hit=None, isolate=None, ab_class=None, pmids=None,
                 notes=None, ref_db=None):
        Gene.__init__(self, unique_id=unique_id, seq_region=seq_region,
                      start=start, end=end, hit=hit, isolate=isolate,
                      ref_db=ref_db)
        Resistance.__init__(self, ab_class=ab_class, pmids=pmids, notes=notes)


class Mutation(Gene):
    """
    """
    def __init__(self, unique_id, seq_region=None, pos=None, hit=None,
                 ref_codon=None, mut_codon=None, ref_aa=None,
                 ref_aa_right=None, mut_aa=None, isolate=None, insertion=None,
                 deletion=None, end=None, nuc=False, premature_stop=0,
                 frameshift=None, ref_db=None, nuc_format=None, aa_format=None):
        Gene.__init__(self, unique_id=unique_id, seq_region=seq_region,
                      start=pos, end=end, hit=hit, isolate=isolate,
                      ref_db=ref_db)
        if(pos is not None):
            self.pos = int(pos)
        self.ref_codon = Feature.na2none(ref_codon)
        self.mut_codon = Feature.na2none(mut_codon)
        self.ref_aa = Feature.na2none(ref_aa)
        self.ref_aa_right = Feature.na2none(ref_aa_right)
        self.mut_aa = Feature.na2none(mut_aa)
        self.nuc = Feature.na2none(nuc)
        self.insertion = Feature.na2none(insertion)
        self.deletion = Feature.na2none(deletion)
        # Indicate how many percent the region was truncated.
        self.premature_stop = Feature.na2none(premature_stop)
        self.frameshift = Feature.na2none(frameshift)
        #key format for indels
        self.nuc_format = nuc_format
        self.aa_format = aa_format

        # Create mutation description
        if(insertion is True and deletion is True):
            self.set_mut_str_delins()
        elif(insertion is True):
            self.set_mut_str_ins()
        elif(deletion is True):
            self.set_mut_str_del()
        else:
            self.set_mut_str_sub()

        self.mut_string = (
            "{region}:{mut_str_short}"
            .format(region=self.seq_region,
                    mut_str_short=self.mut_string_short))

    def set_mut_str_delins(self):
        # Nucleotide mutation
        if(self.nuc):
            # Multiple consecutive deletions (and one or more insertions)
            if(self.end):
                self.mut_string_short = (
                    "g.{pos}_{end}delins{mut}"
                    .format(pos=self.pos, end=self.end,
                            mut=self.mut_codon.upper()))
            # Single deletion (and 1< insertions)
            else:
                self.mut_string_short = (
                    "g.{pos}delins{mut}".format(pos=self.pos,
                                                mut=self.mut_codon.upper()))
        # Amino acid mutation
        else:
            # Multiple consecutive deletions (and one or more insertions)
            if(self.end):
                self.mut_string_short = (
                    "p.{ref}{pos}_{ref_right}{end}delins{mut}"
                    .format(ref=self.ref_aa.upper(), pos=self.pos,
                            ref_right=self.ref_aa_right, end=self.end,
                            mut=self.mut_aa.upper()))
            # Single deletion (and 1< insertions)
            else:
                self.mut_string_short = (
                    "p.{ref}{pos}delins{mut}"
                    .format(ref=self.ref_aa.upper(), pos=self.pos,
                            mut=self.mut_aa.upper()))

    def set_mut_str_ins(self):
        # Nucleotide mutation
        if(self.nuc):
            self.mut_string_short = (
                "g.{pos}_{end}ins{codon}"
                .format(pos=self.pos, end=(self.pos + 1),
                        codon=self.mut_codon.upper()))
        # Amino acid mutation
        else:
            self.mut_string_short = (
                "{ref_left}{pos}_{ref_right}{end}ins{codon}"
                .format(ref_left=self.ref_aa, pos=self.pos,
                        ref_right=self.ref_aa_right,
                        end=(self.pos + 1), codon=self.mut_aa.upper()))

    def set_mut_str_del(self):
        # Nucleotide mutation
        if(self.nuc):
            # Multiple consecutive deletions
            if(self.end):
                self.mut_string_short = (
                    "g.{pos}_{end}del".format(pos=self.pos, end=self.end))
            # Single deletion
            else:
                self.mut_string_short = (
                    "g.{pos}del{codon}".format(pos=self.pos,
                                               codon=self.ref_codon.upper()))
        # Amino acid mutation
        else:
            # Multiple consecutive deletions
            if(self.end):
                self.mut_string_short = (
                    "p.{ref}{pos}_{ref_right}{end}del"
                    .format(pos=self.pos, end=self.end,
                            ref=self.ref_aa.upper(),
                            ref_right=self.ref_aa_right))

            # Single deletion
            else:
                self.mut_string_short = (
                    "p.{ref}{pos}del".format(pos=self.pos,
                                             ref=self.ref_aa.upper()))

    def set_mut_str_sub(self):
        # Nucleotide mutation
        if(self.nuc):
            self.mut_string_short = (
                "g.{pos}{ref}>{mut}"
                .format(pos=self.pos, ref=self.ref_codon.upper(),
                        mut=self.mut_codon.upper()))
        # Amino acid mutation
        else:
            self.mut_string_short = (
                "p.{ref}{pos}{mut}"
                .format(ref=self.ref_aa.upper(), pos=self.pos,
                        mut=self.mut_aa.upper()))


class ResMutation(Mutation, Resistance):
    """
    """
    def __init__(self, unique_id, seq_region=None, pos=None, hit=None,
                 ref_codon=None, mut_codon=None, ref_aa=None,
                 ref_aa_right=None, mut_aa=None, isolate=None, insertion=None,
                 deletion=None, end=None, nuc=False, premature_stop=False,
                 frameshift=None, ab_class=None, pmids=None, notes=None,
                 ref_db=None, nuc_format=None, aa_format=None):
        Mutation.__init__(self, unique_id=unique_id, seq_region=seq_region,
                          pos=pos, hit=hit, ref_codon=ref_codon,
                          mut_codon=mut_codon, ref_aa=ref_aa,
                          ref_aa_right=ref_aa_right, mut_aa=mut_aa,
                          isolate=isolate, insertion=insertion,
                          deletion=deletion, end=end, nuc=nuc,
                          premature_stop=premature_stop, frameshift=frameshift,
                          ref_db=ref_db, nuc_format=nuc_format,
                          aa_format=aa_format)
        Resistance.__init__(self, ab_class=ab_class, pmids=pmids, notes=notes)
