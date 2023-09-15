import bcrypt from 'bcryptjs';
import { SHA256 } from 'crypto-js';

/*export function hashify(password){
//const plainPassword = 'myPassword';
// Generate a salt
const salt = bcrypt.genSaltSync(10);
// Hash the password using the generated salt
const hashedPassword = bcrypt.hashSync(password, salt);
// Send the hashed password to the server or use it in your client-side logic
return hashedPassword
    }*/

export function hashify(value) {
        const hashedValue = SHA256(value).toString();
        return hashedValue;
      }

export function unhashify(password,passwordhash){

    const isMatch = bcrypt.compareSync(password,passwordhash);
    if (isMatch){
        return true
    }
    else {
        return false
    }
}