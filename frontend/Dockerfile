# Use Node.js as base image
FROM node:16

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json to install dependencies first
COPY package.json package-lock.json /app/

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . /app

# Expose the React app port
EXPOSE 3000

# Start the React app
CMD ["npm", "start"]
