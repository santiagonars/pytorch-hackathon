// let observers: Array<(isLogged: boolean) => void> = [];
let observers = [];

const USER_DATA_KEY = 'USER_DATA'

const UserService = {
    subscribe(observer){
        observers.push(observer);
    },

    unsubscribe(observer){
        observers = observers.filter(_observer => _observer !== observer);
    },

    notify(){
        const isLoggedIn = this.isLoggedIn();
        observers.forEach(observer => observer(isLoggedIn));
    },

    getUserData() {
        let data = localStorage.getItem(USER_DATA_KEY)
        return data ? JSON.parse(data) : null
    },

    setUserData(data) {
        if (data) {
            localStorage.setItem(USER_DATA_KEY, JSON.stringify(data));
        } else {
            localStorage.removeItem(USER_DATA_KEY);
        }
        this.notify()
    },

    isLoggedIn: function() {

        let userData = this.getUserData()

        // Have user data?
        if(!userData){
            return false
        }
        
        return true
        // TODO: Uncomment to consider expirationDate of userData
        // // Is expired?
        // let now = new Date().getTime()
        // let tokenExpiresAt = new Date(userData.expireAt).getTime()
        // return now < tokenExpiresAt
    },

    getUsername: function() {
        let data = this.getUserData()
        return data?.username
    },

    getUserId: function() {
        let data = this.getUserData()
        return data?.id
    },

    getToken: function() {
        let data = this.getUserData()
        return data?.token
    },

    logOut: function() {
        this.setUserData(null)
    }
};

export default UserService;