import axios from "axios";

//Возможно, эта штука пригодится
//По крайней мере, я думала ее использовать для проверки авторизации
//https://www.youtube.com/watch?v=uqpM7WVTKI4&ab_channel=ScalableScripts 30:00 (примерно)
axios.defaults.baseURL = "http://localhost:8080";
axios.defaults.headers.common["Authorization"] = "Bearer " + localStorage.getItem("token");