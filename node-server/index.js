const express = require('express')
const cors    = require('cors')
const app     = express()
const axios   = require('axios')
const server  = require('http').createServer(app)
const djangoServer = 'http://localhost:8000/'
const io      = require('socket.io')(server, {
    cors: { origin: "*", methods: ["GET", "POST"] }
})


// enable cors for all origins
app.use(cors("*"))

// tell server to accept json format
app.use(express.json())

// listening to the port
server.listen(3000, () => {console.log("Development server started")})

io.on('connection', (socket) => {

    socket.on('join-room', (roomId, roomVirtualId, roomOwnerId, userId, userPeerId, userAccessToken) => {
        socket.join(roomVirtualId)
        socket.broadcast.to(roomVirtualId).emit('user-connected', userPeerId)

        socket.on('disconnect', () => { 
            if (roomOwnerId == userId) {
                socket.broadcast.to(roomVirtualId).emit('end-call-connection')
                axios.post(djangoServer + 'api/delete-room/', {
                    room_id: roomId
                },
                {
                    headers: { 'Authorization': `Bearer ${userAccessToken}` }
                })
                .then(() => {})
            }
            else {
                socket.broadcast.to(roomVirtualId).emit('user-disconnected', userPeerId, userId)
            }
        })
        
        socket.on('end-call', () => {
            socket.broadcast.to(roomVirtualId).emit('end-call-connection')
        })
        socket.on('send-new-message', (message) => {
            socket.broadcast.to(roomVirtualId).emit('new-message', message)
        })

    })
})