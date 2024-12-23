const mongoose = require('mongoose');

const categorySchema = new mongoose.Schema({
    title: {
        type: String,
        required: true,
        maxLength: 200
    },
    parent: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Category',
        default: null
    },
    path: [{
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Category'
    }],
    level: {
        type: Number,
        default: 0
    }
}, {
    timestamps: true
});

categorySchema.pre('save', async function (next) {
    if (this.parent) {
        const parent = await this.constructor.findById(this.parent);
        if (parent) {
            this.path = [...parent.path, parent._id];
            this.level = parent.level + 1;
        }
    } else {
        this.path = [];
        this.level = 0;
    }
    next();
});

module.exports = mongoose.model('Category', categorySchema); 