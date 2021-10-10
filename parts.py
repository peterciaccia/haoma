"""
Created on 2021-10-08 by Peter Ciaccia

Part class declarations
"""
import dogma

class Part:
    def __init__(self, seqrecord, material='dna'):
        """
        needs:

        :param seqrecord:
        """
        self.fiveprime_required = False
        self.threeprime_required = False

        # TODO: instantiation must check that "Part" on either side is set
        # Can only be instantiated after additional conditions met, like end part or adjacent part
        self.fiveprime_interface = PartInterface
        self.threeprime_interface = PartInterface

        self.material = material
        self.seqrecord = seqrecord

        # TODO: Implement genetic dependencies. Does not consider cofactor dependencies
        self.dependencies = []


class Promoter(Part):

    def __init__(self, seqrecord):
        super().__init__(seqrecord)
        self.threeprime_required = True


class Terminator(Part):

    def __init__(self, seqrecord):
        super().__init__(seqrecord)
        self.fiveprime_required = True
        self.function = dogma.StopTranscription()


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