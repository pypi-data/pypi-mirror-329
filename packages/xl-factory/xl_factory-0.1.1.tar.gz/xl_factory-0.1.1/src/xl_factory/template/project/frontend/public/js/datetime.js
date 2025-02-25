import dayjs from 'dayjs';

// 基础格式化函数
const formatDatetime = date => dayjs(date).format('YYYY-MM-DD HH:mm:ss');
const formatDate = date => dayjs(date).format('YYYY-MM-DD');

// 获取当前时间
const getToday = () => dayjs().format('YYYY-MM-DD');
const getNow = () => dayjs().format('YYYY-MM-DD HH:mm:ss');

// 通用时间计算函数
const addTime = (unit, amount) => {
    return dayjs().add(amount, unit).format('YYYY-MM-DD');
}

// 周相关
const getNextWeek = () => addTime('week', 1);
const getWeekLater = (n) => addTime('week', n);

// 月相关
const getMonthLater = (n) => addTime('month', n);
const getOneMonthLater = () => getMonthLater(1);
const getTwoMonthLater = () => getMonthLater(2);
const getThreeMonthLater = () => getMonthLater(3);
const getFourMonthLater = () => getMonthLater(4);
const getFiveMonthLater = () => getMonthLater(5);
const getSixMonthLater = () => getMonthLater(6);
const getSevenMonthLater = () => getMonthLater(7);
const getEightMonthLater = () => getMonthLater(8);
const getNineMonthLater = () => getMonthLater(9);
const getTenMonthLater = () => getMonthLater(10);
const getElevenMonthLater = () => getMonthLater(11);

// 季度相关
const getQuarterLater = (n) => getMonthLater(n * 3);
const getOneQuarterLater = () => getQuarterLater(1);
const getTwoQuarterLater = () => getQuarterLater(2);
const getThreeQuarterLater = () => getQuarterLater(3);

// 半年
const getHalfYearLater = () => getMonthLater(6);

// 指定日期的n天后
const nDaysLater = (dateStr, n) => {
    return dayjs(dateStr).add(n, 'day').format('YYYY-MM-DD');
}

export default {
    // 基础格式化
    formatDate,
    formatDatetime,

    // 当前时间
    getToday,
    getNow,

    // 周相关
    getNextWeek,
    getWeekLater,

    // 月相关
    getMonthLater,
    getOneMonthLater,
    getTwoMonthLater,
    getThreeMonthLater,
    getFourMonthLater,
    getFiveMonthLater,
    getSixMonthLater,
    getSevenMonthLater,
    getEightMonthLater,
    getNineMonthLater,
    getTenMonthLater,
    getElevenMonthLater,

    // 季度相关
    getOneQuarterLater,
    getTwoQuarterLater,
    getThreeQuarterLater,

    // 半年
    getHalfYearLater,

    // 指定日期计算
    nDaysLater
}
