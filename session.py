import json, datetime, os

class Session:

    data = {}
    path = None
    unsaved = True
    updated_at = None

    def __init__(self):
        """Initialize session class"""
        self.created_at = datetime.datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')

    def __repr__(self):
        """Return a printable representation of this instance
        
        Returns:
            str
        """
        return json.dumps(self.all)

    def __str__(self):
        """Return a formatted printable representation of this instance
        
        Returns:
            str
        """
        return json.dumps(self.all, indent=4)

    @property
    def all(self):
        """Get full session data as dictionary
        
        Returns:
            dict
        """
        return {
            'data': self.data, 
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    def get(self, name, fallback=None):
        """Get session value

        Arguments:
            name {str} -- variable name
            fallback {mixed} -- fallback value if variable doesn't exist

        Returns:
            mixed
        """
        return self.data.get(name, fallback)

    def set(self, name, value):
        """Set session value

        Arguments:
            name {str} -- variable name
            value {mixed}
        """
        self.data[name] = value
        self.updated_at = datetime.datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
        self.unsaved = True

    def load(self, data:dict):
        """Load session data from variable
        
        Arguments:
            data {dict} -- keyworded session data
        """
        self.data = data
        self.updated_at = datetime.datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
        self.unsaved = True
    
    def save(self, name):  
        """Write session data to a .sav file

        Arguments:
            name {str} -- file name
        """    
        sav = self.savfile(name)
        json.dump(self.all, sav)        
        self.unsaved = False
        sav.close()

    def read(self, name):
        """Read session data from a .sav file

        Arguments:
            name {str} -- file name
        """
        sav = self.savfile(name, 'r')
        data = json.load(sav)
        self.data = data['data']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.unsaved = False        
        sav.close()        

    def savfile(self, name, mode='w+'):
        """Open save file

        Arguments:
            name {str} -- file name
            mode {str} -- open mode

        Returns:
            _io.TextIOWrapper
        """
        path = f'saves/{name}.sav'
        if 'w' in mode:
            os.makedirs(os.path.dirname(path), exist_ok=True)
        self.path = path
        return open(path, mode)
