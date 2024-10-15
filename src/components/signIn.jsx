import React, { useState } from 'react';
import axios from 'axios';
function ConnexionForm() {
    const [formData, setFormData] = useState({
        password: '',
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };


    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/login', formData, {
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            alert(response.data.message);
        } catch (error) {
            console.error("Erreur lors de la connexion :", error);
        }
    };

    return (
        <div style={styles.container}>

            <h2 style={styles.h2}>CONNEXION</h2>

            <form style={styles.form}>
                <div style={styles.label}>



                    <input type="password" name="password" value={formData.password} placeholder='     mot de passe' isRequired={true} onChange={handleChange} style={styles.input} />

                </div>



                <button type="submit" style={styles.btn} onClick={handleSubmit}>Se connecter</button>

            </form>



        </div>
    );
}

const styles = {
    container: {
        width: '30%',
        height: '40vh',

        fontFamily: 'Arial, sans-serif',
        backgroundColor: '#fff',
        borderRadius: '10px',
        boxShadow: '0px 0px 15px rgba(0, 0, 0, 0.1)',
        position: 'center',
        transform: 'translate(120%,55%)'
    },
    h2: {
        transform: 'translate(0%,50%)',
        color: 'orange',
    },
    form: {
        display: 'flex',
        flexDirection: 'column',     // Aligner les éléments en colonne
        width: '90%',
        height: '90%',              // Largeur du formulaire
        // Ajoute du padding autour du formulaire

    },
    label: {
        padding: '10px',
    },
    input: {
        marginLeft: '5px',
        width: '70%',
        height: '6vh',
        border: '1px solid orange',
        transform: 'translate(10%,100%)',
        borderRadius: '5px',

    },
    btn: {
        padding: '10px 20px',
        borderRadius: '5px',
        backgroundColor: '#FFA500',
        color: '#fff',
        border: 'none',
        cursor: 'pointer',
        height: '5vh',
        width: '40%',
        transform: 'translate(90%,300%)',

    }

}

export default ConnexionForm;
