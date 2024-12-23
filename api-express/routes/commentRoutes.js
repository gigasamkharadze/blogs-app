const express = require('express');
const router = express.Router();
const { protect } = require('../middleware/authMiddleware');
const {
    createComment,
    getComments,
    updateComment,
    deleteComment,
    likeComment,
    dislikeComment
} = require('../controllers/commentController');

router.route('/:blogId/comments')
    .get(getComments)
    .post(protect, createComment);

router.route('/:blogId/comments/:commentId')
    .put(protect, updateComment)
    .delete(protect, deleteComment);

router.route('/:blogId/comments/:commentId/like')
    .post(protect, likeComment);

router.route('/:blogId/comments/:commentId/dislike')
    .post(protect, dislikeComment);

module.exports = router;