# Dockerfile frontend

# Start from a base image
FROM node:14

# Set working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of your app's source code from your host to your image filesystem.
COPY . .

# Expose the port
EXPOSE 3000

# Command to start the application
CMD ["npm", "start"]
