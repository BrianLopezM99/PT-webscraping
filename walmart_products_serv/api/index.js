import { spawn } from 'child_process';
import express from 'express'
import dotenv from 'dotenv'

const app = express();

dotenv.config({path: '../.env'})

app.get('/', (req, res) => {
  res.send('Hola, mundo!');
});

const puerto = process.env.PORT || 3000;

app.listen(puerto, () => {
  console.log(`Servidor iniciado en http://localhost:${puerto}`);
});

app.get('/api/:parametro', (req, res) => {
    const parametro = req.params.parametro;
  
    // Ejecute el script de Python y pase el parámetro
    const proceso = spawn('python', ['../python_scraping/walmart_products.py', parametro]);
  
    // Capture la salida del proceso de Python y responda con ella
    proceso.stdout.on('data', (datos) => {
      res.send(datos.toString());
    });
  });
