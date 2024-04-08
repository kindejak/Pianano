# Pianano

# Pianano

Pianano is a Django web application designed to provide teachers with device management capabilities and an API for accessing device-related data.

## Features

- Device Management: Teachers can add, view, update, and delete devices used in their classrooms.
- API: Pianano provides a RESTful API that allows developers to comunicate with pianano device

## Installation

1. Clone the repository: `git clone https://github.com/kindejak/pianano.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Set up the database: `python manage.py migrate`
4. Start the development server: `python manage.py runserver`

## Usage

1. Access the web app by visiting `http://localhost:8000` in your browser.
2. Sign in with your teacher account or create a new one.
3. Use the intuitive interface to manage your devices and view device-related data.
4. To access the API, refer to the API documentation at `http://localhost:8000/api/docs`.

## Contributing

Contributions are welcome! If you'd like to contribute to Pianano, please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit them: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.