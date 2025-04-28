const path = require('path');

module.exports = {
    entry: 'D:\\CleanSlate\\_AppBuild\\Javascript\\JSX Files\\Backend Interface\\EmployeeApp.jsx',
    // adjust if your path is slightly different
  output: {
    path: path.resolve(__dirname, 'Javascript/Bundles'),
    filename: 'employeeApp.bundle.js',
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-react'],
          },
        },
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],
  },
  mode: 'development',
};
