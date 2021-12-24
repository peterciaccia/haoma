"""
Created on 2021-10-08 by Peter Ciaccia

Part class declarations
"""
import dogma
import log.conf


class Part:
    def __init__(self, seqrecord, material='dna'):
        """
        needs:

        :param seqrecord:
        """

        self.logger = log.conf.get_logger(Part)
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

        self.logger = log.conf.get_logger(Promoter)
        self.threeprime_required = True


class Terminator(Part):

    def __init__(self, seqrecord):
        super().__init__(seqrecord)

        self.logger = log.conf.get_logger(Terminator)
        self.fiveprime_required = True
        self.function = dogma.StopTranscription()


class Cds(Part):

    def __init__(self, seqrecord):
        super().__init__(seqrecord)

        self.logger = log.conf.get_logger(Cds)
        self.fiveprime_required = True
        self.threeprime_required = True


class PartInterface:
    def __init__(self, fiveprimepart=None, threeprimepart=None):

        self.logger = log.conf.get_logger(PartInterface)

        if fiveprimepart is None and threeprimepart is None:
            raise ValueError(f'A PartInterface instance requires either the five prime part or the three prime part '
            f'not to be {None}')


class PartSchema:
    """
    Defines part architecture
    :param system: instance or declaration of System child class
    :param schema: tuple of Part objects
    """
    def __init__(self, schema, system, schema_id=None):

        # system defines the part environment, usually means an organism, e.g. E. coli MG1655
        if schema_id is None:
            self.schema_id = 1
        else:
            self.schema_id = schema_id

        self._schema = schema
        self.system = system

    def get_schema(self):
        return self._schema
    def set_schema(self, schm):
        self._schema = schm
    schema = property(get_schema, set_schema)

    # TODO: Import schema IDs from directory ?

    def get_draft_sequence(self, *args):
        seqs = ''.join(str(x.seq) for x in args)
        return seqs
