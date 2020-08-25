import Axios from "axios";
import UserService from "./UserService";

const apiUrl = process.env.REACT_APP_API_BASE_URL+process.env.REACT_APP_API_NAMESPACE

let userId = UserService.getUserId()
const listener = (newIsLogged) => {
    userId = UserService.getUserId()
}
UserService.subscribe(listener)

const ApiService = {

    login: function(userName, password) {
        return Axios.post(`${apiUrl}/auth/login`, {
            userName: userName,
            password: password
        }).catch(err => {
            console.error(err)
            throw err
        })
    },
    
    register: function(userName, password) {
        return Axios.post(`${apiUrl}/auth/register`, {
            userName: userName,
            password: password
        }).catch(err => {
            console.error(err)
            throw err
        })
    },

    getProjects: function() {    
        return Axios.get(`${apiUrl}/users/${userId}/projects`)
        .then(res => {
            if(res.status >= 200 && res.status < 300){
                return res.data.projects
            } else {
                throw new Error("getProjects", res)
            }
        })
        .catch(err => {
            console.error(err)
            throw err
        })
    },
    getProject: function(id) {
        return Axios.get(`${apiUrl}/users/${userId}/projects/${id}`)
        .then(res => {
            if(res.status >= 200 && res.status < 300){
                return res.data.project
            } else {
                throw new Error("getProject", res)
            }
        })
        .catch(err => {
            console.error(err)
            throw err
        })
    },
    createProject: function(projectName) {
        return Axios.post(`${apiUrl}/users/${userId}/projects`, {name: projectName})
        .then(res => {
            if(res.status >= 200 && res.status < 300){
                return res.data.project
            } else {
                throw new Error("createProject", res)
            }
        })
        .catch(err => {
            console.error(err)
            throw err
        })
    },
    getImages: function(projectId) {
        return Axios.get(`${apiUrl}/users/${userId}/projects/${projectId}/images`)
        .then(res => {
            if(res.status >= 200 && res.status < 300){
                return res.data.images
            } else {
                throw new Error("getImages", res)
            }
        })
        .catch(err => {
            console.error(err)
            throw err
        })
    },
    postImages: function(projectId, images) {
        const formData = new FormData()
        formData.append(
            'images',
            images
        )

        return Axios.post(
            `${apiUrl}/users/${userId}/projects/${projectId}/images`,
            formData
        ).then(res => {
            if(res.status >= 200 && res.status < 300){
                return res
            } else {
                throw new Error("postImages", res)
            }
        }).catch(err => {
            console.error(err)
            throw err
        })
    },
    // getImage: function(projectId, imageId) {
    // },
    deleteImage: function(projectId, imageId) {
        return Axios.delete(
            `${apiUrl}/users/${userId}/projects/${projectId}/images/${imageId}`,
        ).then(res => {
            if(res.status >= 200 && res.status < 300){
                return res
            } else {
                throw new Error("deleteImage", res)
            }
        }).catch(err => {
            console.error(err)
            throw err
        })
    },
    postJob: function(projectId) {
        return Axios.post(`${apiUrl}/users/${userId}/projects/${projectId}/job`)
        .then(res => {
            if(res.status >= 200 && res.status < 300){
                return res.data // Correct?
            } else {
                throw new Error("postJob", res)
            }
        })
        .catch(err => {
            console.error(err)
            throw err
        })
    }
};

export default ApiService;