# README.md

This is basically the methodology I've used from this point on. In prose, that is. 

1. We have two datasets sitting in here. Below is a brief description of each, along with a link to the paper that describes them. 
	a. TalkBank (in particular DementiaBank) is a shared database of multimedia interactions for the study of communication in dementia. The English subset presents 5 different studies, 4 of which were useful to this project. 
		https://dementia.talkbank.org/access/
	b. Talk2Me is a crowd-sourced data set of volunteer speakers who self-assign their diagnosis. This is mostly used as a control group for us. 
		https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0212342

2. These data contain a multiple recordings for basically two classes: Control and Diagnosed. This is an oversimplification that I'll need to get into with the actual writing. But there are 1136 Diagnosed recordings totalling 37.061 hours and 14330 Control recordings totalling 19.693 hours. To further complicate the matter, most of the Diagnosed recordings from the TalkBank (DementiaBank) corpus are compressed .mp3 format. So, we have selected the usable 855 Diagnosed .wav files and the remaining 281 Diagnosed .mp3 files which add up to 12.798 hours of speech. Then we have randomly sampled from the Control .wav files to come up with 15.348 hours of speech. This satisfies the class imbalance issue without undue use of .mp3 compressed formatting files. 

3. Transcriptions are not available for these data. So, instead, the Kaldi ASPIRE speech recognizer was used to get a transcript of uttered words. This process has multiple steps which are outlined below. 

	a. First run setUp4Convert.py. This gets everything ready to be turned into 8khz
	b. Then run convert.sh (twice) to change all of the copied files from CHUNKS into their 8khz formats
	c. Then run setUp4Try.py. This gets a list of all the absolute paths to the file names which aspire needs.
	d. Then run try.sh in the following nohup command:
        nohup bash try.sh & > output.log 2>&1
   You do this after having replaced the textfile name for either Diagnosed or Control.
	e. Then run extractFromNohup.py. This will make a CSV with file IDs and transcriptions.
	f. Take those transcriptions back to the other folder and figure out forced alignment.

4. Once transcriptions had been acquired for each of the files, they were force-aligned using the Montreal Forced Aligner. This was accomplished at the phone and word levels because they are necessary to be able to split the files to a single word and also to be able to extract vowel quality measures. 

5. With the phone-level alignments, it was possible to then split the audio files on word boundaries calculated from the Forced Aligner. This results in a CSV of file name identifiers (locations) and the individual word they are ascribed to. An arbitrary threshold was decided upon to filter out uncommon words and unknown phrases. 

6. A single dataframe was then constructed from the audio which measured the following features: 
	a. # zero-crossings
	b. Dynamic range of amplitude
	c. Normalized energy (using RMS) using a loudness model
	d. 5 Spectral moments
		i. Center of Gravity
		ii. Skewness
		iii. Kurtosis
		iv. Central moment
		v. Standard deviation
	e. Speech to Noise Ratio
		i. 0 dB SNR
			x. Speech-weighted noise masker
			y. Modulated noise masker
		ii. -6 dB SNR
			x. Speech-weighted noise masker
			y. Modulated noise masker
		iii. -12 dB SNR
			x. Speech-weighted noise masker
			y. Modulated noise masker
	f. Averaged vowel duration
	g. Averaged Vowel Space Measurements
		i. F1
		ii. F2
		iii. F3
	All of these features were collected, in addition to information about Speaker age, sex (if known). Also which collection it came from, the diagnosis, the encoding, and the speaker ID. 

7. This dataframe was then used to present a series of input vectors to multiple machine learning paradigms. The following were used: 

	a. From Sci-Kit Learn
		i. Dummy
		ii. Nearest neighbors
		iii. Linear SVM
		iv. RBF SVM
		v. Gaussian Process
		vi. Decision Tree
		vii. Random Forest
		viii. Neural Net
		ix. ADA Boost
		x. Naive Bayes
		xi. QDA
	b. From PyTorch
		i. Feed Forward Neural Network
		ii. Recurrent Neural Network

8. Somewhere in here I need to run PCA to figure out which features are the most valuable. But then I also should just do a 'pull one out' method on the classifiers. 
