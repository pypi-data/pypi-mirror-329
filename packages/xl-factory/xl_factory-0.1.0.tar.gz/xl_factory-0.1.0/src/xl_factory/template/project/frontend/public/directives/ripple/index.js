import './style.css'

export const ripple = {
    mounted(el) {
        el.style.position = 'relative'
        el.style.overflow = 'hidden'

        el.addEventListener('click', (e) => {
            const rect = el.getBoundingClientRect()
            const size = Math.max(el.offsetWidth, el.offsetHeight)

            const ripple = document.createElement('span')
            ripple.className = 'ripple'

            // 设置涟漪元素的大小
            ripple.style.width = ripple.style.height = `${size}px`

            // 计算涟漪的位置，使其以点击位置为中心
            const x = e.clientX - rect.left - size / 2
            const y = e.clientY - rect.top - size / 2

            ripple.style.left = `${x}px`
            ripple.style.top = `${y}px`

            // 移除已存在的涟漪
            const existingRipple = el.querySelector('.ripple')
            if (existingRipple) {
                existingRipple.remove()
            }

            el.appendChild(ripple)

            // 动画结束后移除涟漪元素
            ripple.addEventListener('animationend', () => {
                ripple.remove()
            })
        })
    }
}