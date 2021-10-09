"""
Created on 2021-10-08 by Peter Ciaccia

Part class declarations
"""


class Part:
    def __init__(self, seqrecord, material='dna'):
        """
        needs:

        :param sequence:
        """
        self.fiveprime_required = False
        self.threeprime_required = False

        # TODO: instantiation must check that "Part" on either side is set
        # Can only be instantiated after additional conditions mets, like end part or adjacent part
        self.fiveprime_interface = PartInterface
        self.threeprime_interface = PartInterface

        self.material = material
        self.seqrecord = seqrecord


class Promoter(Part):

    def __init__(self, seqrecord):
        super().__init__(seqrecord)
        self.threeprime_required = True


class Terminator(Part):

    def __init__(self, seqrecord):
        super().__init__(seqrecord)
        self.fiveprime_required = True


class Cds(Part):

    def __init__(self, seqrecord):
        super().__init__(seqrecord)
        self.fiveprime_required = True
        self.threeprime_required = True


class PartInterface:
    def __init__(self, fiveprimepart=None, threeprimepart=None):

        if fiveprimepart is None and threeprimepart is None:
            raise ValueError(f'A PartInterface instance requires either the five prime part or the three prime part '
            f'not to be {None}')