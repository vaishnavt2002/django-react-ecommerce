export function setVerificationId(id) {
    sessionStorage.setItem("verification_id", id)
}

export function getVerificationId() {
    return sessionStorage.getItem("verification_id")
}

export function clearVerificationId(){
    return sessionStorage.removeItem("verification_id")
}