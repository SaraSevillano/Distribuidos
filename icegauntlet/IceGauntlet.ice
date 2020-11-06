module IceGauntlet{

    exception Unauthorized{
        string razon;
    };

    exception RoomAlReadyExists{
        string razon;
    }:

    exception RoomNotExists{
        string razon;
    };
    
    interface Authentication{
        void changePassword (string user, string currentPassHash, string newPassHash) throws Unauthorized;

        string getNewToken(string user, string passwordHash) throws Unauthorized;

        bool isValid (string token);
    };

    interface GestionMapas{
        void publish (string token, string roomData) throws Unauthorized, RoomAlReadyExists;

        void remove (string token, string roomName) throws RoomNotExists;
    };

    interface ObtenerMapa{
        string getRoom () throws RoomNotExists;
    }
};