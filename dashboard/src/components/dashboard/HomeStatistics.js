import React, { useEffect, useState } from 'react';
import axiosInstance from '../../axiosInstance';
import { Doughnut, Bar, Pie, Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
} from 'chart.js';
import { Height } from '@mui/icons-material';
import { padding } from '@mui/system';

ChartJS.register(Tooltip, Legend, ArcElement, CategoryScale, LinearScale, BarElement, LineElement, PointElement);

const HomeStatistics = () => {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    axiosInstance.get('stats/', { headers: getAuthHeaders() })
      .then(response => setStats(response.data))
      .catch(error => console.error('Erreur lors de la récupération des statistiques', error));
  }, []);

  if (!stats) {
    return <div style={styles.loading}>Chargement des statistiques...</div>;
  }

  // Données pour les graphiques
  const programData = {
    labels: ['Programme Fitness', 'Programme Nutrition'],
    datasets: [{
      label: 'Nombre de Clients',
      data: [stats.program_fitness_count, stats.program_nutrition_count],
      backgroundColor: ['#3e95cd', '#ff6f61'],
    }],
  };

  const weightData = {
    labels: ['Poids Moyen', 'Poids Cible'],
    datasets: [{
      label: 'Poids',
      data: [stats.avg_weight, stats.avg_goal_weight],
      backgroundColor: ['#ffcc00', '#3e95cd'],
      borderWidth: 1,
    }],
  };

  const genderData = {
    labels: ['Hommes', 'Femmes'],
    datasets: [{
      label: 'Répartition des Sexes',
      data: [stats.male_count, stats.female_count],
      backgroundColor: ['#3e95cd', '#ff6f61'],
      borderWidth: 1,
    }],
  };

  return (
    <div style={styles.container}>
      {/* Cartes pour Âge Moyen et Total Clients */}
      <div style={styles.cardContainer}>
        {/* Total des clients */}
        <div className="card border border-info shadow-0 mb-3" style={styles.card}>
          <div className="card-header">Clients Totals</div>
          <div className="card-body" style={{padding:0}}>
            <h5 className="card-title"style={{padding:0}}>{stats.total_clients}</h5>
          </div>
        </div>

        {/* Âge Moyen */}
        <div className="card border border-info shadow-0 mb-3" style={styles.card}>
          <div className="card-header">Âge Moyen</div>
          <div className="card-body"style={{padding:0}}>
            <h5 className="card-title"style={{padding:0}}>{stats.avg_age}</h5>
          </div>
        </div>
      </div>

      <div style={styles.chartContainer}>
        {/* Programme Fitness vs Nutrition - Graphique en Bar */}
        <div style={styles.chart}>
          <Bar data={programData} options={chartOptions} />
          <p style={styles.chartLabel}>Répartition des Programmes</p>
        </div>

        {/* Poids Moyen vs Poids Cible - Graphique en Line */}
        <div style={styles.chart}>
          <Line data={weightData} options={chartOptions} />
          <p style={styles.chartLabel}>Poids Moyen vs Poids Cible</p>
        </div>

        {/* Répartition des Sexes - Graphique en Pie */}
        <div style={styles.chart}>
          <Pie data={genderData} options={chartOptions} />
          <p style={styles.chartLabel}>Répartition des Sexes</p>
        </div>
      </div>
    </div>
  );
};

// Chart options
const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top',
    },
  },
  scales: {
    x: {
      ticks: {
        font: {
          size: 12,
        },
      },
    },
    y: {
      ticks: {
        font: {
          size: 12,
        },
      },
    },
  },
};

// Styles
const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    marginTop: '20px',
    padding: '20px',
    backgroundColor: '#f9f9f9',
    borderRadius: '12px',
    boxShadow: '0 6px 12px rgba(0, 0, 0, 0.15)',
    maxWidth: '1300px',
    width: '100%',
    marginLeft: 'auto',
    marginRight: 'auto',
    overflow: 'auto',
  },
  loading: {
    fontSize: '1.5rem',
    color: '#007bff',
    textAlign: 'center',
    marginTop: '50px',
  },
  title: {
    fontSize: '2rem',
    fontWeight: 'bold',
    marginBottom: '20px',
    color: '#000000',
    textAlign: 'center',
  },
  cardContainer: {
    display: 'flex',
    justifyContent: 'center',
    gap: '20px',
    marginBottom: '30px', // Space between the cards and charts
  },
  card: {
    width: '15rem',
    height: '6.5rem',
    backgroundColor: '#e7f7ff', // Couleur de fond plus douce
    border: '2px solid #5bc0de', // Bordure avec couleur bleue
    borderRadius: '10px', // Coins arrondis
    display: 'flex', 
    flexDirection: 'column',
    justifyContent: 'center',  // Centrer verticalement
    alignItems: 'center',  // Centrer horizontalement
    padding: '0px',  // Padding supprimé
  },
  cardTitle: {
    fontSize: '2rem', // Taille de police agrandie pour le titre
    fontWeight: 'bold', // Titre en gras
    color: '#000000', // Couleur bleue pour le texte du titre
  },
  cardText: {
    fontSize: '1.25rem', // Augmenter la taille du texte
    color: '#000000', // Couleur du texte
    textAlign: 'center', // Centrer le texte
  },
  chartContainer: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
    gap: '20px',
    width: '80%',
  },
  chart: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    padding: '20px',
    backgroundColor: '#fff',
    borderRadius: '12px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
  },
  chartLabel: {
    textAlign: 'center',
    marginTop: '10px',
    fontSize: '0.9rem',
    color: '#666',
  },
};

const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return token ? { Authorization: `Bearer ${token}` } : {};
};

export default HomeStatistics;
