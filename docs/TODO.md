What needs to be done

[x] Playback
    [x] Communication with Reaper (over http, inspire/copy from Tomas Dudacek)
    [x] Reaper setup guide - see audio_preparation_guide.txt
    [x] Player class - abstraction of a player, able to play samples
    [x] Connection to the UI buttons - class PlaybackControl
[x] User interface
    [x] Choose the library - PyQt6
    [x] Rating input elemnts - LabeledSlider, ButtonRow, RatingWidget
    [x] Sample widget allowing start/stop playback of the correct sample - SampleWidget
    [x] The structure of the test widow - ItemWidget, QuestionWidget, Window
    [x] Signal connection to allowing the collection of results - pyqtSignal ItemWidget.ratingChanged
[x] Collection of the results
    [x] Choose the saving filetype - .csv
    [x] Class accepting UI signals and collecting results - RatingCollector
    [x] Design the result storing format - test_results.csv
[ ] The test logic and global settings
[x] Test settings saving/loading (json/xml)
    [x] Plan the overall structure - sample_settings.json
    [x] Code the parsers & savers for all the objects
[ ] Settings editor



