# Use Node.js as the base image
FROM node:18

# Set the working directory
WORKDIR /usr/src/app

# Copy the frontend code
COPY ./ /usr/src/app

# Set environment to development
ENV NODE_ENV=development

# Install dependencies (including devDependencies)
RUN npm install

# Verify vite installation
RUN npx vite --version

# Expose the frontend port
EXPOSE 3000

# Start the frontend in development mode
CMD ["npm", "run", "dev"]
