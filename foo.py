import numpy as np
from coffea import hist
import coffea.processor as processor
import awkward as ak

class bar(processor.ProcessorABC):
    def __init__(self):
        dataset_axis = hist.Cat("dataset", "")
        MET_axis = hist.Bin("MET", "MET [GeV]", 50, 0, 100)
        
        self._accumulator = processor.dict_accumulator({
            'MET': hist.Hist("Counts", dataset_axis, MET_axis),
            'cutflow': processor.defaultdict_accumulator(int)
        })
    
    @property
    def accumulator(self):
        return self._accumulator
    
    def process(self, events):
        output = self.accumulator.identity()
        
        dataset = events.metadata["dataset"]
        MET = events.MET.pt
        
        output['cutflow']['all events'] += ak.size(MET)
        output['cutflow']['number of chunks'] += 1
        
        output['MET'].fill(dataset=dataset, MET=MET)
        return output

    def postprocess(self, accumulator):
        return accumulator