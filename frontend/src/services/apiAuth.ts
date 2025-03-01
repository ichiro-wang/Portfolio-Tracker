import axios, {isAxiosError} from "axios";

export const signupTest = async () => {
    const res = await axios.post("/api/auth/signup", {name:"Michael Jordan", email: "mj23@gmail.com", password:"michael23"})
    console.log(res)
    return res.data
}

export const loginTest = async () => {
    const res = await axios.post("/api/auth/login", {email: "mj23@gmail.com", password:"michael23"})
    console.log(res)
    return res.data
}

export const logoutTest = async () => {
    const res = await axios.post("/api/auth/logout")
    console.log(res)
    return res.data
}

export const getMeTest = async () => {
    try {
        const res = await axios.get("/api/auth/me")
        console.log(res)
        return res.data
    }
    catch (e: unknown) {
        if (isAxiosError(e)) {
            console.log(e.response?.data)
            return e.response?.data
        }
        else {
            return {error: "Unknown error"}
        }
    }
}
