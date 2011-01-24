from collective.multimodeview.samples.notes_view import NotesView
from persistent.dict import PersistentDict

class McpNotesView(NotesView):
    """ Provides some extra actions than the one defined
    in multimodeview.
    """
    display_zones_list = ['home', 'news', 'control panel']

    def get_display_zones(self):
        metadata = self._get_metadata()

        display_zones = metadata.get('display_zones',
                                     None)
        if display_zones is None:
            metadata['display_zones'] = PersistentDict()
            display_zones = metadata['display_zones']

        return display_zones

    def set_display_zones(self, note_id, zones):
        dzones = self.get_display_zones()
        dzones[note_id] = zones
