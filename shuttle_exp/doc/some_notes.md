# Programming Notes (qupulse)

*It is obvious a good habit to write down some notes during Programming.*

## Installation

> ### Observation:
> `python -m pip install -e .` and `python setup.py develop` are doing different things.

> ### My understand:
> Both of them should make an editable installation with a locally cloned package. However, the former command installed a pre-released version say v-0.7 independent of any changes in the package. The other one works as intended that by making an egg-link in the `site-packages` folder of a `venv` instead of installing a package, all local modification can be reloaded and used by other scripts. 
> - ONLY tested with Jupyter Notebook in VS Code. `python 3.7.9` in a virtual environment is used.

## Usage

### n_segment
> What is `n_segment` in some early pulse definitions?  
> For example: HDAWG has `n_segment = 192` where $192 = 3*2^6$... What does 3 mean? And 6 bits?
> The following code in `qupulse.hardware.awg.zihdawg.py`... I don't understand... `WAVEFORM_LEN_QUANTUM = 16`? 4 bits of what?
````python
class HDAWGChannelGroup(AWG):
    MIN_WAVEFORM_LEN = 192
    WAVEFORM_LEN_QUANTUM = 16
````

### Measureemnt window
> Why do we define measurement window by qupulse? Can't we just let qupulse make a pulse and directly use atsAverage for data acquisation and downsampling so that less inteference between pulse generation and date acquisation for both soft- & hardware? It is for sure handled by qupulse now to forward the position and length of measurement masks to alazar such that the card will know when to do what kinds of operation for how long time, however, it is deeply hidden in packages. Any tutorials about that?  
> Now I'm confused by the definition and functionality of **BufferStrategy, Mask, Buffer and Operation**. It wouldn't be better to have a concrete documentation or at least doc strings for `qupulse.hardware.dacs.alazar`.  
>> Simon: atsaverage gets the ScanlineConfiguration from the qupulse driver. Thats it. Rest is magic.    
>> Q: what about mask?  
>> Simon: Its all to assemble the ScanlineConfiguration, which requires masks and operations.



