
from .utils import loadDefault

class Language:
    """ Language settings """

    default = {
        "sample" : "#Sample",
        "end test" : "#End the test",
        "fillall errtitle" : "#Not all ratings filled",
        "fillall errmessage" : "#All questions are required to be filled in the test. End it anyway?",
        "save errtitle" : "#Results saving failed",
        "save errmessage" : "#An error occurred while saving the results. Exit without saving?",
        "warning box title" : "#Warning",
        "reaper error" : "#Failed to connect to the Reaper",
        "note" : "#Note"
    }

    def __init__(self, lang : dict):
        lang = loadDefault(lang, Language.default)
        self.sample = lang["sample"]
        self.endTest = lang["end test"]
        self.fillAllErrTitle = lang["fillall errtitle"]
        self.fillAllErrMessage = lang["fillall errmessage"]
        self.saveErrTitle = lang["save errtitle"]
        self.saveErrMessage = lang["save errmessage"]
        self.warningBoxTitle = lang["warning box title"]
        self.reaperError = lang["reaper error"]
        self.note = lang["note"]

    def toDict(self) -> dict:
        data = {}
        data["sample"] = self.sample
        data["end test"] = self.endTest
        data["fillall errtitle"] = self.fillAllErrTitle
        data["fillall errmessage"] = self.fillAllErrMessage
        data["save errtitle"] = self.saveErrTitle
        data["save errmessage"] = self.saveErrMessage
        data["warning box title"] = self.warningBoxTitle
        data["reaper error"] = self.reaperError
        data["note"] = self.note
        return data

LanguageEN = Language({
    "sample" : "Track",
    "end test" : "Finish the test",
    "fillall errtitle" : "Ratings not filled",
    "fillall errmessage" : "All questions are required to be answered in the test. Are you sure you want to end it anyway?",
    "save errtitle" : "Results saving error",
    "save errmessage" : "An error occurred while saving the results. Exit without saving?",
    "warning box title" : "Warning",
    "reaper error" : "The connection to Reaper is lost, playback is not available.",
    "note" : "Note"
})

LanguageCZ = Language({
    "sample" : "Stopa",
    "end test" : "Ukončit test",
    "fillall errtitle" : "Nevyplněné hodnocení",
    "fillall errmessage" : "Všechny otázky v testu musí být zodpovězeny. Opravdu chcete test ukončit nyní?",
    "save errtitle" : "Chyba uložení výsledků",
    "save errmessage" : "Při ukládání výsledků došlo k chybě. Ukončit test bez uložení?",
    "warning box title" : "Chyba",
    "reaper error" : "Nepodařilo se navázat spojení s programem Reaper, nelze přehrávat vzorky.",
    "note" : "Poznámka"
})

LanguageDefault = LanguageEN

LanguageList = {
    "EN" : LanguageEN,
    "CZ" : LanguageCZ
}
