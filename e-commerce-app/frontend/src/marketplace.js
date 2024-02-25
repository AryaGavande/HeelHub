const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors()); // This will enable CORS for all routes and origins

// You can also configure CORS for specific routes and origins
app.use(cors({
  origin: 'http://localhost:5501/e-commerce-app/frontend/homescreen.html', // Allow only this origin to access
  methods: 'GET,POST,PUT,DELETE', // Allow only these methods
  allowedHeaders: 'Content-Type,Authorization', // Allow only these headers
  credentials: true, // Allow cookies
}));

app.get('/data', (req, res) => {
  res.json({ data: 'This is CORS-enabled for all origins!' });
});

app.listen(3000, () => console.log('Server running on port 3000'));

public void ConfigureServices(IServiceCollection, services)
{
    services.AddCors(options =>
    {
        options.AddPolicy("MyCorsPolicy",
            builder => builder.WithOrigins("http://example.com")
                .AllowAnyMethod()
                .AllowAnyHeader()
                .AllowCredentials());
    });
}
public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
{
    app.UseCors("MyCorsPolicy"); // Use the CORS policy

    // Other configurations...
}
