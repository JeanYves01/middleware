import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';  // Import useNavigate pour rediriger
import axios from 'axios';
function InscriptionForm() {
    const [formData, setFormData] = useState({
        nom: '',
        prenom: '',
        email: ''
    });
    // const navigate = useNavigate();  // Hook pour la redirection

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:5001/signupForm', formData, {
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            alert(response.data.message);
            // Redirection vers la page de connexion
            window.location.href = '/signIn';  // Ou l'URL correspondant à votre page de connexion
        } catch (error) {
            console.error("Erreur lors de l'inscription :", error);
        }
    };

    return (
        <div style={styles.container}>
            <h2 style={styles.h2}>INSCRIPTION</h2>
            <form style={styles.form} onSubmit={handleSubmit}>
                <div style={styles.label}>
                    <input type="text" name="nom" value={formData.nom} onChange={handleChange} placeholder='     Votre nom' style={styles.input} />
                </div>
                <div style={styles.label}>
                    <input type="text" name="prenom" value={formData.prenom} onChange={handleChange} placeholder='     Votre prénom' style={styles.input} />
                </div>
                <div style={styles.label}>
                    <input type="email" name="email" value={formData.email} onChange={handleChange} placeholder='     Votre email' style={styles.input} />
                </div>
                <button type="submit" style={styles.btn} onClick={handleSubmit}>S'inscrire</button>
            </form>
        </div>
    );
}

const styles = {
    container: {
        width: '30%',
        height: '65vh',

        fontFamily: 'Arial, sans-serif',
        backgroundColor: '#fff',
        borderRadius: '10px',
        boxShadow: '0px 0px 15px rgba(0, 0, 0, 0.1)',
        position: 'center',
        transform: 'translate(120%,15%)'
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
        padding: '20px',
    },
    input:{
        marginLeft: '5px',
        width: '70%',
        height: '5vh',
        border: '1px solid orange',
        transform: 'translate(10%,70%)',
        borderRadius: '5px',
    },
    btn: {
        padding: '10px 20px',
        borderRadius: '5px',
        backgroundColor: '#FFA500',
        color: '#fff',
        border: 'none',
        cursor: 'pointer',
        height:'5vh',
        width: '40%',
        transform: 'translate(90%,120%)',
        fontSize: '15px',
        fontWeigth: 'bold',
        textAlign:'center'
    }

}

export default InscriptionForm;
