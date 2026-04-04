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
    [x] How to save unfilled fields
[ ] The test logic and global settings
[ ] Test settings saving/loading (json/xml)
    [x] Plan the overall structure - sample_settings.json
    [x] Code the parsers & savers for all the objects
[ ] Settings editor


[ ] Fixes
    [ ] Connect the Finish Test button
    [ ] Add logging to PlaybackControl

[ ] Features
    [x] Language settings
    [x] Playback volume
    [x] Sample names (no / track # / from .json)
    [x] Shuffle samples (yes / no)
    [x] Listening order (forced linear / can repeat current sample / free)
    [x] Display previous scores (yes / no)
    [ ] Rate only after finished listening (yes / no)
    [ ] Change the rating afterwards (yes / no)
    [ ] Force to fill everything
    [ ] Allow stop

[ ] Additional
    [ ] Double comparison samples
    [ ] Shuffle comparison samples
    [ ] Color themes


