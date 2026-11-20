// ==================== 游戏全局状态 ====================
let gameState = {
    day: 1,
    money: 0,
    timeLeft: 300,
    timerInterval: null,
    currentVisitor: null,
    visitedToday: 0,
    totalVisitorsToday: 10,
    upgrades: {
        quickBookmarks: false,
        advancedDorm: false,
        stickyNote: false,
        autoTrade: false
    },
    confiscatedItems: [],
    helpCount: 0,
    corruption: 0,
    route: null,
    simpleMode: true,
    phoneCallActive: false,
    phoneCallback: null,
    newspaperShownToday: false,
    hasFakeLetter: false,
    hasTicket: false,
    escapeReady: false,
    gameDate: new Date(2026, 2, 1),
    tutorialShown: false,
    compareMode: false,
    compareFirstField: null,
    day25EventTriggered: false,
    phoneConfirmedForged: false,
    mails: [],
    nextMailId: 1,
    phoneNumbers: null,
    wantedList: [],
    stocks: [
        { name: "实验科技", code: "SY001", price: 5.00, prevPrice: 5.00, positions: [] },
        { name: "深中贸易", code: "SZ002", price: 8.50, prevPrice: 8.50, positions: [] },
        { name: "深高级制造", code: "SG003", price: 12.00, prevPrice: 12.00, positions: [] },
        { name: "实验金融", code: "SY004", price: 9.50, prevPrice: 9.50, positions: [] },
        { name: "深外基建", code: "SW005", price: 7.50, prevPrice: 7.50, positions: [] }
    ],
    stockNews: "",
    lastStockUpdateDay: 0,
    trainingCompleted: false,
    trainingPhoneNumber: "0755-00000000",
    playerName: "检察员",
    talent: null,
    achievements: {
        firstArrest: false,
        firstPhoneCall: false,
        firstStockTrade: false,
        firstHelpOrganization: false,
        firstConfiscation: false,
        firstTenCorrect: false,
        millionaire: false,
        perfectDay: false,
        stockMaster: false,
        undercover: false,
        whistleblower: false,
        survivalist: false,
        fugitive: false,
        revolutionary: false,
        loyalist: false,
        confiscator: false,
        corrupt: false
    },
    correctCount: 0,
    totalEarned: 0,
    stockProfit: 0,
    compareUsed: false,
    confiscatedNormalLetters: 0,
    escapePlanAvailable: false,
    canCheck: true
};

let triggeredEvents = [];

const SCHOOLS = ['深圳实验中学', '深圳中学', '深圳高级中学', '深圳外国语学校', '教育局直属中学'];

const propagandaNews = [
    "校长强调：严格遵守防疫规定，戴口罩、勤洗手。",
    "校园文化艺术节将于下周举行，欢迎同学们踊跃报名。",
    "食堂推出新菜品，健康又美味，欢迎品尝。",
    "本周六举行消防安全演练，请同学们做好准备。",
    "图书馆延长开放时间，方便同学们复习备考。"
];

const flavorEvents = [
    "一只橘猫跑进了检查站，你不得不花时间赶走它。",
    "一名学生递给你一瓶水，说“辛苦了”。",
    "窗外下起了大雨，你想起自己没带伞。",
    "广播里播放着校长的讲话，内容是鼓励大家好好学习。",
    "一个低年级学生怯生生地问你：“检察员同学，我学生证照片掉了怎么办？”",
    "你的椅子突然摇晃了一下，差点摔倒。",
    "食堂阿姨给你送来一份免费午餐。",
    "一个学生对你敬礼，说“感谢你的辛勤工作”。"
];

const financialNews = [
    { text: "实验科技发布新产品，股价大涨！", effect: { "实验科技": 1.08 } },
    { text: "深中贸易出口受阻，股价下跌。", effect: { "深中贸易": 0.93 } },
    { text: "深高级制造获得大订单，股价上升。", effect: { "深高级制造": 1.07 } },
    { text: "实验金融业绩超预期，股价上涨。", effect: { "实验金融": 1.06 } },
    { text: "深外基建中标新项目，股价飙升。", effect: { "深外基建": 1.10 } },
    { text: "市场整体回调，所有股票小幅下跌。", effect: { "all": 0.97 } },
    { text: "政府出台利好政策，股市普涨。", effect: { "all": 1.04 } },
    { text: "行业竞争加剧，科技股承压。", effect: { "实验科技": 0.94 } },
    { text: "贸易摩擦缓和，深中贸易反弹。", effect: { "深中贸易": 1.05 } }
];

// ==================== 辅助函数 ====================
function formatTime(seconds) {
    let mins = Math.floor(seconds / 60);
    let secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

function updateDateDisplay() {
    const year = gameState.gameDate.getFullYear();
    const month = (gameState.gameDate.getMonth() + 1).toString().padStart(2, '0');
    const day = gameState.gameDate.getDate().toString().padStart(2, '0');
    const dateStr = `${year}-${month}-${day}`;
    document.getElementById('date-display').innerText = `日期: ${dateStr}`;
    document.getElementById('current-date-value').innerText = dateStr;
}

function updateUI() {
    document.getElementById('day').innerText = gameState.day;
    document.getElementById('time-left').innerText = formatTime(gameState.timeLeft);
    document.getElementById('money').innerText = Math.floor(gameState.money);
    document.getElementById('player-name-display').innerText = gameState.playerName;
    updateDateDisplay();
    
    const confiscatePanel = document.getElementById('confiscated-panel');
    if (gameState.day >= 25) {
        confiscatePanel.style.display = 'block';
        updateConfiscatedList();
    } else {
        confiscatePanel.style.display = 'none';
    }
    
    const arrestBtn = document.getElementById('btn-arrest');
    if (gameState.phoneConfirmedForged && gameState.currentVisitor && gameState.currentVisitor.forged) {
        arrestBtn.style.display = 'inline-block';
    } else {
        arrestBtn.style.display = 'none';
    }
    
    const oldConfiscateBtn = document.getElementById('btn-confiscate');
    if (oldConfiscateBtn) oldConfiscateBtn.style.display = 'none';
    
    renderUpgradePanel();
    updateBrowserAccess();
    updatePhoneShortcuts();
    updateStockUI();
}

function updateBrowserAccess() {
    const browserUnlockDiv = document.getElementById('browser-unlock');
    const browserContentDiv = document.getElementById('browser-content');
    if (gameState.upgrades.quickBookmarks) {
        browserUnlockDiv.style.display = 'none';
        browserContentDiv.style.display = 'block';
    } else {
        browserUnlockDiv.style.display = 'block';
        browserContentDiv.style.display = 'none';
    }
}

function showMessage(msg, color = '#ffffff', duration = 2000) {
    const msgDiv = document.getElementById('message');
    msgDiv.innerHTML = msg;
    msgDiv.style.color = color;
    setTimeout(() => {
        if (document.getElementById('message').innerHTML === msg) {
            msgDiv.innerHTML = '';
        }
    }, duration);
}

function unlockAchievement(achKey, achName) {
    if (!gameState.achievements[achKey]) {
        gameState.achievements[achKey] = true;
        showMessage(`🏆 成就解锁：${achName}`, '#ffcc00', 4000);
    }
}

function applyTalent() {
    if (gameState.talent === 'economic') {
        showMessage('天赋[经济头脑]生效：房租水电减半，简单模式每日补贴+10元', '#88ff88', 4000);
    } else if (gameState.talent === 'justice') {
        showMessage('天赋[正义感]生效：正确审核+5元，逮捕额外+10元', '#88ff88', 4000);
    } else if (gameState.talent === 'insight') {
        showMessage('天赋[洞察力]生效：首次对比不耗时间，股票波动缩小30%', '#88ff88', 4000);
    }
}

// ==================== 禁用/启用操作按钮 ====================
function disableActionButtons() {
    document.querySelectorAll('#action-buttons .action').forEach(btn => {
        if (btn.id !== 'btn-next-student') {
            btn.disabled = true;
            btn.style.opacity = '0.5';
            btn.style.cursor = 'default';
        }
    });
}

function enableActionButtons() {
    document.querySelectorAll('#action-buttons .action').forEach(btn => {
        if (btn.id !== 'btn-next-student') {
            btn.disabled = false;
            btn.style.opacity = '1';
            btn.style.cursor = 'pointer';
        }
    });
}

// ==================== 随机电话号码 ====================
function randomPhoneSuffix() {
    return Math.floor(100000 + Math.random() * 900000).toString();
}

function generatePhoneNumbers() {
    return {
        edu: "0755-" + randomPhoneSuffix(),
        principal_sy: "0755-" + randomPhoneSuffix(),
        principal_sz: "0755-" + randomPhoneSuffix(),
        principal_sg: "0755-" + randomPhoneSuffix(),
        principal_wgy: "0755-" + randomPhoneSuffix(),
        principal_jyj: "0755-" + randomPhoneSuffix(),
        report: "0755-" + randomPhoneSuffix()
    };
}

// ==================== 股票系统 ====================
function updateStockUI() {
    const tbody = document.getElementById('stock-tbody');
    if (tbody) {
        tbody.innerHTML = '';
        gameState.stocks.forEach((stock) => {
            const row = tbody.insertRow();
            row.insertCell(0).innerText = stock.name;
            row.insertCell(1).innerText = stock.price.toFixed(2);
            let change = 0, changePercent = 0;
            let changeText = '--', percentText = '--';
            if (stock.prevPrice !== undefined) {
                change = stock.price - stock.prevPrice;
                changePercent = (change / stock.prevPrice) * 100;
                changeText = (change > 0 ? '+' : '') + change.toFixed(2);
                percentText = (changePercent > 0 ? '+' : '') + changePercent.toFixed(2) + '%';
            }
            row.insertCell(2).innerText = changeText;
            row.insertCell(3).innerText = percentText;
            const btnCell = row.insertCell(4);
            const tradeBtn = document.createElement('button');
            tradeBtn.innerText = '交易';
            tradeBtn.className = 'small-btn';
            tradeBtn.onclick = () => prepareTrade(stock.name);
            btnCell.appendChild(tradeBtn);
        });
    }
    const newsDiv = document.getElementById('stock-news');
    if (newsDiv) newsDiv.innerText = gameState.stockNews || "暂无金融新闻";
    
    const select = document.getElementById('stock-select');
    if (select) {
        const currentVal = select.value;
        select.innerHTML = '';
        gameState.stocks.forEach(s => {
            const opt = document.createElement('option');
            opt.value = s.name;
            opt.innerText = `${s.name} (${s.price.toFixed(2)})`;
            select.appendChild(opt);
        });
        if (currentVal && gameState.stocks.some(s => s.name === currentVal)) {
            select.value = currentVal;
        }
    }
    
    const currentStockName = select ? select.value : (gameState.stocks[0]?.name);
    const stock = gameState.stocks.find(s => s.name === currentStockName);
    const sellSelect = document.getElementById('sell-position-select');
    if (sellSelect) {
        sellSelect.innerHTML = '<option value="">选择持仓</option>';
        if (stock && stock.positions.length > 0) {
            stock.positions.forEach((pos, idx) => {
                const opt = document.createElement('option');
                opt.value = idx;
                opt.innerText = `杠杆${pos.leverage}x, ${pos.shares}份, 开仓价${pos.openPrice.toFixed(2)}`;
                sellSelect.appendChild(opt);
            });
        }
        const tradeType = document.getElementById('trade-type')?.value;
        sellSelect.style.display = tradeType === 'sell' ? 'inline-block' : 'none';
    }
    
    const holdingsDiv = document.getElementById('holdings');
    if (holdingsDiv) {
        let html = "持仓明细:<br>";
        let hasAny = false;
        gameState.stocks.forEach(s => {
            if (s.positions.length > 0) {
                s.positions.forEach(pos => {
                    html += `${s.name} [${pos.leverage}x] ${pos.shares}份 @${pos.openPrice.toFixed(2)}<br>`;
                    hasAny = true;
                });
            }
        });
        if (!hasAny) html += "无";
        holdingsDiv.innerHTML = html;
    }
}

function prepareTrade(stockName) {
    const select = document.getElementById('stock-select');
    if (select) select.value = stockName;
    const priceInput = document.getElementById('trade-price');
    const volumeInput = document.getElementById('trade-volume');
    if (gameState.upgrades.autoTrade) {
        const stock = gameState.stocks.find(s => s.name === stockName);
        if (priceInput) priceInput.value = stock ? stock.price.toFixed(2) : '';
        if (volumeInput) volumeInput.value = 1;
    } else {
        if (priceInput) priceInput.value = '';
        if (volumeInput) volumeInput.value = '';
    }
    updateStockUI();
}

function executeTrade() {
    const select = document.getElementById('stock-select');
    const type = document.getElementById('trade-type').value;
    let price = parseFloat(document.getElementById('trade-price').value);
    let volume = parseInt(document.getElementById('trade-volume').value);
    const stockName = select.value;
    const stock = gameState.stocks.find(s => s.name === stockName);
    if (!stock) { showMessage("股票不存在", "#ff8888"); return; }
    if (isNaN(volume) || volume <= 0) { showMessage("数量必须为正整数", "#ff8888"); return; }
    if (isNaN(price) || price <= 0) { showMessage("请输入有效价格", "#ff8888"); return; }
    
    const minPrice = stock.price * 0.5;
    const maxPrice = stock.price * 2.0;
    if (price < minPrice || price > maxPrice) {
        showMessage(`价格必须在当前价 ${stock.price.toFixed(2)} 的 50%~200% 之间 (${minPrice.toFixed(2)} ~ ${maxPrice.toFixed(2)})`, "#ff8888", 3000);
        return;
    }
    
    if (type === 'buy') {
        const leverageSelect = document.getElementById('leverage-select');
        let leverage = leverageSelect ? parseInt(leverageSelect.value) : 1;
        if (isNaN(leverage) || leverage < 1) leverage = 1;
        const totalValue = price * volume * 10;
        const margin = totalValue / leverage;
        if (gameState.money >= margin) {
            gameState.money -= margin;
            stock.positions.push({
                leverage: leverage,
                shares: volume,
                openPrice: price
            });
            showMessage(`买入 ${stockName} ${volume}份，杠杆${leverage}x，保证金 ${margin.toFixed(2)}元`, "#88aa88");
            if (!gameState.achievements.firstStockTrade) unlockAchievement('firstStockTrade', '初入股市');
        } else {
            showMessage("保证金不足", "#ff8888");
            return;
        }
    } else if (type === 'sell') {
        const sellSelect = document.getElementById('sell-position-select');
        const posIndex = parseInt(sellSelect.value);
        if (isNaN(posIndex) || posIndex < 0 || posIndex >= stock.positions.length) {
            showMessage("请选择要卖出的持仓", "#ff8888");
            return;
        }
        const pos = stock.positions[posIndex];
        if (pos.shares < volume) {
            showMessage(`持仓不足，当前持有 ${pos.shares} 份`, "#ff8888");
            return;
        }
        const totalValue = price * volume * 10;
        const profit = (price - pos.openPrice) * volume * 10 * pos.leverage;
        const marginUsed = (pos.openPrice * volume * 10) / pos.leverage;
        gameState.money += marginUsed + profit;
        gameState.stockProfit += profit;
        if (volume === pos.shares) {
            stock.positions.splice(posIndex, 1);
        } else {
            pos.shares -= volume;
        }
        showMessage(`卖出 ${stockName} ${volume}份，盈亏 ${profit.toFixed(2)}元`, profit >=0 ? "#88aa88" : "#ff8888");
        if (!gameState.achievements.firstStockTrade) unlockAchievement('firstStockTrade', '初入股市');
        if (gameState.stockProfit >= 500 && !gameState.achievements.stockMaster) unlockAchievement('stockMaster', '股神');
    }
    updateUI();
}

function checkLiquidation() {
    let liquidated = false;
    for (let s of gameState.stocks) {
        for (let i = 0; i < s.positions.length; i++) {
            const pos = s.positions[i];
            const margin = (pos.openPrice * pos.shares * 10) / pos.leverage;
            const loss = (pos.openPrice - s.price) * pos.shares * 10;
            if (loss > margin) {
                const totalLoss = loss;
                gameState.money -= totalLoss;
                showMessage(`[爆仓] 您的 ${s.name} 杠杆${pos.leverage}x 持仓被强制平仓，亏损 ${totalLoss.toFixed(2)} 元！`, "#ff4444", 4000);
                s.positions.splice(i, 1);
                i--;
                liquidated = true;
            }
        }
    }
    if (liquidated) updateUI();
    if (gameState.money < 0) debtEnding();
}

function updateStockPrices() {
    if (gameState.lastStockUpdateDay === gameState.day) return;
    gameState.lastStockUpdateDay = gameState.day;
    gameState.stocks.forEach(s => {
        s.prevPrice = s.price;
    });
    let news = null;
    if (Math.random() < 0.4) {
        news = financialNews[Math.floor(Math.random() * financialNews.length)];
        gameState.stockNews = news.text;
        if (news.effect["all"]) {
            gameState.stocks.forEach(s => {
                let factor = news.effect["all"];
                if (gameState.talent === 'insight') factor = 1 + (factor - 1) * 0.7;
                s.price = s.price * factor;
            });
        } else {
            for (let [name, factor] of Object.entries(news.effect)) {
                const stock = gameState.stocks.find(s => s.name === name);
                if (stock) {
                    if (gameState.talent === 'insight') factor = 1 + (factor - 1) * 0.7;
                    stock.price = stock.price * factor;
                }
            }
        }
    } else {
        gameState.stockNews = "今日无重要金融新闻，市场平稳。";
        gameState.stocks.forEach(s => {
            let change = (Math.random() - 0.5) * 0.1;
            if (gameState.talent === 'insight') change = change * 0.7;
            s.price = s.price * (1 + change);
        });
    }
    gameState.stocks.forEach(s => {
        if (s.price < 0.1) s.price = 0.1;
        s.price = Math.round(s.price * 100) / 100;
    });
    checkLiquidation();
    updateStockUI();
}

// ==================== 通缉令系统 ====================
function generateWantedList() {
    const wanted = [];
    const count = Math.floor(Math.random() * 2) + 1;
    for (let i = 0; i < count; i++) {
        wanted.push({
            name: generateRandomName(),
            studentId: "2024" + Math.floor(Math.random() * 10000).toString().padStart(4,'0'),
            reason: "参与违纪活动"
        });
    }
    return wanted;
}

function checkIfWanted(visitor) {
    return gameState.wantedList.some(w => w.name === visitor.name && w.studentId === visitor.studentId);
}

// ==================== 风味事件 ====================
function triggerFlavorEvent() {
    if (Math.random() < 0.5) {
        const event = flavorEvents[Math.floor(Math.random() * flavorEvents.length)];
        showMessage(`[校园轶事] ${event}`, '#aaccee', 4000);
    }
}

// ==================== 邮件系统 ====================
function showMailNotification(subject, sender) {
    let notification = document.getElementById('mail-notification');
    if (!notification) {
        notification = document.createElement('div');
        notification.id = 'mail-notification';
        notification.style.position = 'fixed';
        notification.style.bottom = '20px';
        notification.style.right = '20px';
        notification.style.background = '#e8dcbc';
        notification.style.border = '2px solid #7a5a4a';
        notification.style.padding = '10px';
        notification.style.zIndex = '3000';
        notification.style.fontFamily = 'monospace';
        notification.style.fontSize = '12px';
        notification.style.boxShadow = '4px 4px 0 rgba(0,0,0,0.3)';
        notification.style.cursor = 'pointer';
        document.body.appendChild(notification);
    }
    notification.innerHTML = `<strong>📧 新邮件</strong><br>发件人: ${sender}<br>主题: ${subject}<br><span style="font-size:10px;">点击查看</span>`;
    notification.style.display = 'block';
    notification.onclick = () => {
        openMailbox();
        notification.style.display = 'none';
    };
    setTimeout(() => {
        if (notification) notification.style.display = 'none';
    }, 3000);
}

function addMail(subject, content, isEvent = false, eventData = null, sender = null) {
    const mail = {
        id: gameState.nextMailId++,
        subject: subject,
        content: content,
        date: new Date().toLocaleString(),
        isEvent: isEvent,
        eventData: eventData,
        sender: sender,
        read: false
    };
    gameState.mails.push(mail);
    updateMailIcon();
    showMailNotification(subject, sender || '系统');
}

function updateMailIcon() {
    const unread = gameState.mails.filter(m => !m.read).length;
    const mailboxBtn = document.getElementById('mailbox-btn');
    if (mailboxBtn) {
        if (unread > 0) {
            mailboxBtn.innerText = `📧 收件箱 (${unread})`;
        } else {
            mailboxBtn.innerText = `📧 收件箱`;
        }
    }
}

function openMailbox() {
    const modal = document.getElementById('mailbox-modal');
    const mailListDiv = document.getElementById('mail-list');
    mailListDiv.innerHTML = '';
    if (gameState.mails.length === 0) {
        mailListDiv.innerHTML = '<div>暂无邮件</div>';
    } else {
        gameState.mails.forEach(mail => {
            const mailDiv = document.createElement('div');
            mailDiv.className = 'mail-item';
            mailDiv.innerHTML = `
                <div class="mail-subject">${mail.subject}</div>
                <div class="mail-date">${mail.date}</div>
                <div style="font-size:12px; margin-top:4px;">${mail.content.substring(0, 80)}${mail.content.length>80?'...':''}</div>
            `;
            mailDiv.onclick = () => openMail(mail);
            mailListDiv.appendChild(mailDiv);
        });
    }
    modal.style.display = 'flex';
}

function openMail(mail) {
    if (!mail.read) {
        mail.read = true;
        updateMailIcon();
    }
    if (mail.isEvent && mail.eventData) {
        const modal = document.getElementById('mail-action-modal');
        document.getElementById('mail-subject').innerText = mail.subject;
        document.getElementById('mail-body').innerHTML = `<p style="color: #aa4444;"><strong>⚠️ 该邮件为风险邮件，请拨打纪检部电话举报。</strong></p><p>${mail.content}</p>`;
        const actionsDiv = document.getElementById('mail-actions');
        actionsDiv.innerHTML = '';
        const deleteBtn = document.createElement('button');
        deleteBtn.innerText = '删除邮件';
        deleteBtn.onclick = () => {
            modal.style.display = 'none';
            const index = gameState.mails.findIndex(m => m.id === mail.id);
            if (index !== -1) gameState.mails.splice(index, 1);
            updateMailIcon();
            showMessage('邮件已删除。', '#cccccc');
        };
        const replyBtn = document.createElement('button');
        replyBtn.innerText = '回复邮件';
        replyBtn.onclick = () => {
            modal.style.display = 'none';
            gameState.helpCount++;
            showMessage('你回复了邮件，帮助了学生斗争委员会。', '#88aa88');
            const index = gameState.mails.findIndex(m => m.id === mail.id);
            if (index !== -1) gameState.mails.splice(index, 1);
            updateMailIcon();
            if (!gameState.achievements.firstHelpOrganization) unlockAchievement('firstHelpOrganization', '暗中支持');
            if (gameState.helpCount >= 5 && !gameState.achievements.undercover) unlockAchievement('undercover', '地下工作者');
        };
        const exitBtn = document.createElement('button');
        exitBtn.innerText = '退出';
        exitBtn.onclick = () => {
            modal.style.display = 'none';
        };
        actionsDiv.appendChild(deleteBtn);
        actionsDiv.appendChild(replyBtn);
        actionsDiv.appendChild(exitBtn);
        modal.style.display = 'flex';
    } else {
        alert(`【${mail.subject}】\n\n${mail.content}`);
    }
}

function sendDailyMail() {
    const requiredDocs = [];
    requiredDocs.push("学生证");
    if (gameState.day >= 3) requiredDocs.push("校园卡(实验) / 临时通行证(外校)");
    if (gameState.day >= 8) requiredDocs.push("纪检部准入证(外校)");
    if (gameState.day >= 15) requiredDocs.push("转学介绍信(转学生)");
    if (gameState.day >= 20) requiredDocs.push("健康证明(健康状态)");
    const content = `今日余额: ${Math.floor(gameState.money)} 元\n今日需要检查的文件: ${requiredDocs.join('、')}\n请仔细核对证件，注意伪造特征。`;
    addMail(`第${gameState.day}天 执勤简报`, content);
}

function checkOrganizationEvents() {
    const events = [
        { id: "first_contact", day: 3, title: "匿名邮件", desc: "我们需要你的帮助。如果你愿意，今晚7点在校门口小卖部见。" },
        { id: "corridor_talk", day: 7, title: "走廊对话", desc: "一个学生悄悄对你说：“检察员同学，您知道宿舍热水总停吗？我们想写联名信，您能帮我们递给校长吗？”" },
        { id: "fundraising", day: 12, title: "募捐活动", desc: "一个学生塞给你一个信封，里面是“学生斗争委员会”的募捐信，希望筹集资金印刷刊物。" },
        { id: "cover_action", day: 18, title: "掩护行动", desc: "检查一名学生时，校警突然闯入，要求你配合检查该学生的书包。学生紧张地看着你。" },
        { id: "core_mission", day: 22, title: "核心任务", desc: "组织成员希望你帮忙从教务处电脑里拷贝一份学生处分记录，用于揭露不公。" },
        { id: "revolution_eve", day: 28, title: "革命前夜", desc: "组织负责人亲自来找你，告知即将发动和平抗议，希望你届时站在他们一边。" }
    ];
    const event = events.find(e => e.day === gameState.day && !triggeredEvents.includes(e.id));
    if (event) {
        triggeredEvents.push(event.id);
        addMail(`[深圳学生斗争委员会] ${event.title}`, event.desc, true, event, "深圳学生斗争委员会");
    }
}

// ==================== 报纸系统 ====================
function showNewspaper(callback) {
    let newsText = "";
    if (gameState.day === 3) {
        newsText = "[新规] 从今日起，本校学生须出示校园卡，外校学生须出示临时通行证。";
    } else if (gameState.day === 8) {
        newsText = "[新规] 外校学生须出示纪检部准入证，并说明入校目的。";
    } else if (gameState.day === 15) {
        newsText = "[新规] 转学目的需提供转学介绍信，须双方校长签字。";
    } else if (gameState.day === 20) {
        newsText = "[新规] 近期伪造介绍信猖獗，即日起可没收伪造介绍信（不罚款）。但没收真实介绍信将罚款25元。请仔细核对！";
    } else if (gameState.day === 25) {
        newsText = "[提醒] 近期发现大量伪造介绍信，请仔细核对签名。";
    } else {
        newsText = propagandaNews[Math.floor(Math.random() * propagandaNews.length)];
    }
    
    const modal = document.getElementById('newspaper-modal');
    const contentDiv = document.getElementById('newspaper-content');
    contentDiv.innerHTML = `<p>${newsText}</p>`;
    modal.style.display = 'flex';
    const closeBtn = document.getElementById('close-newspaper');
    const handler = () => {
        modal.style.display = 'none';
        closeBtn.removeEventListener('click', handler);
        if (callback) callback();
    };
    closeBtn.addEventListener('click', handler);
}

function showTutorialContent(callback) {
    const modal = document.getElementById('tutorial-modal');
    const contentDiv = document.getElementById('tutorial-content');
    contentDiv.innerHTML = `
        <p><strong>纪检部培训内容：</strong></p>
        <p>1. <strong>检查学生证</strong>：核对姓名、年级、出生日期、学号、有效期、学校。</p>
        <p>2. <strong>识别伪造</strong>：注意出生日期与年级是否匹配（七年级应约2013年出生）。学号应与入学年份匹配（七年级2025，八年级2024，九年级2023）。</p>
        <p>3. <strong>额外文件</strong>：根据天数不同，可能需要校园卡、临时通行证、准入证、转学介绍信、健康证明等。</p>
        <p>4. <strong>电脑查询</strong>：点击“打开浏览器”可查阅学校信息、电话簿、准入规定。购买“快捷收藏夹”后无需每次打开浏览器。</p>
        <p>5. <strong>电话核实</strong>：遇到可疑身份，可拨打电话核实（购买“便签”升级后可一键拨打常用电话）。</p>
        <p>6. <strong>升级与费用</strong>：每天扣除房租水电，正确审核获得收入。可用金钱购买升级（快捷收藏夹、高级宿舍、便签）。</p>
        <p>7. <strong>对比检查</strong>：点击“对比模式”后，可依次点击两个字段进行智能比对（年级vs出生日期、有效期vs今天日期等）。</p>
        <p>8. <strong>邮件系统</strong>：计算机中有收件箱，每日会收到系统邮件，重要事件也会以邮件形式通知。</p>
        <p>9. <strong>股票交易</strong>：可购买/卖出股票，支持杠杆（最高5倍）。升级“一键填写交割单”可简化操作。</p>
        <p><em>培训结束，祝工作顺利！</em></p>
    `;
    modal.style.display = 'flex';
    const closeBtn = document.getElementById('close-tutorial');
    const handler = () => {
        modal.style.display = 'none';
        closeBtn.removeEventListener('click', handler);
        if (callback) callback();
    };
    closeBtn.addEventListener('click', handler);
}

function showNote(callback) {
    const modal = document.getElementById('note-modal');
    modal.style.display = 'flex';
    const closeBtn = document.getElementById('close-note');
    const handler = () => {
        modal.style.display = 'none';
        closeBtn.removeEventListener('click', handler);
        if (callback) callback();
    };
    closeBtn.addEventListener('click', handler);
}

function showTrainingCall() {
    if (gameState.trainingCompleted) {
        showMessage('该号码已失效，培训已完成。', '#ffaa88');
        return;
    }
    const modal = document.getElementById('phone-oneclick-modal');
    const numberSpan = document.getElementById('call-number');
    const resultDiv = document.getElementById('oneclick-result');
    numberSpan.innerText = gameState.trainingPhoneNumber;
    resultDiv.innerHTML = '正在接通纪检部培训专线...';
    modal.style.display = 'flex';
    setTimeout(() => {
        resultDiv.innerHTML = '接通成功！请听培训内容：';
        setTimeout(() => {
            modal.style.display = 'none';
            showTutorialContent(() => {
                gameState.trainingCompleted = true;
                showMessage('培训完成！现在可以正式开始执勤了。', '#88aa88', 3000);
                updateUI();
                const trainingBtn = document.getElementById('training-btn');
                if (trainingBtn) trainingBtn.remove();
                updatePhoneShortcuts();
            });
        }, 1500);
    }, 1000);
    const closeBtn = document.getElementById('oneclick-close');
    const handler = () => {
        modal.style.display = 'none';
        closeBtn.removeEventListener('click', handler);
    };
    closeBtn.addEventListener('click', handler);
}

function showPhoneShortcut(number, visitor) {
    if (!gameState.trainingCompleted && gameState.day === 1 && number === gameState.trainingPhoneNumber) {
        showTrainingCall();
        return;
    }
    const modal = document.getElementById('phone-oneclick-modal');
    const numberSpan = document.getElementById('call-number');
    const resultDiv = document.getElementById('oneclick-result');
    numberSpan.innerText = number;
    resultDiv.innerHTML = '正在接通...';
    modal.style.display = 'flex';
    setTimeout(() => {
        const isGenuine = !visitor.forged || Math.random() < 0.3;
        if (isGenuine) {
            resultDiv.innerHTML = '对方反馈：证件信息真实有效。';
            gameState.phoneConfirmedForged = false;
        } else {
            resultDiv.innerHTML = '对方反馈：查无此人或证件不符，疑似伪造。';
            gameState.phoneConfirmedForged = true;
        }
        setTimeout(() => {
            modal.style.display = 'none';
            updateUI();
        }, 2000);
    }, 1500);
    const closeBtn = document.getElementById('oneclick-close');
    const handler = () => {
        modal.style.display = 'none';
        closeBtn.removeEventListener('click', handler);
    };
    closeBtn.addEventListener('click', handler);
    if (!gameState.achievements.firstPhoneCall) unlockAchievement('firstPhoneCall', '第一次通话');
}

function showPhoneInputModal(visitor, callback) {
    if (gameState.upgrades.stickyNote) {
        if (!gameState.trainingCompleted && gameState.day === 1) {
            showTrainingCall();
            callback(true);
        } else {
            showPhoneShortcut(gameState.phoneNumbers?.edu || '0755-12345678', visitor);
            callback(true);
        }
    } else {
        const modal = document.getElementById('phone-input-modal');
        const input = document.getElementById('phone-number-input');
        const confirmBtn = document.getElementById('confirm-phone-btn');
        const cancelBtn = document.getElementById('cancel-phone-btn');
        const resultDiv = document.getElementById('phone-result');
        
        input.value = '';
        resultDiv.innerHTML = '';
        modal.style.display = 'flex';
        
        const onConfirm = () => {
            const enteredNumber = input.value.trim();
            if (!gameState.trainingCompleted && gameState.day === 1 && enteredNumber === gameState.trainingPhoneNumber) {
                modal.style.display = 'none';
                showTrainingCall();
                confirmBtn.removeEventListener('click', onConfirm);
                cancelBtn.removeEventListener('click', onCancel);
                return;
            }
            const correctNumber = gameState.phoneNumbers ? gameState.phoneNumbers.edu : '0755-12345678';
            if (enteredNumber === correctNumber) {
                resultDiv.innerHTML = '正在接通教育局...';
                resultDiv.style.color = '#a8e0a8';
                setTimeout(() => {
                    const isGenuine = !visitor.forged || Math.random() < 0.3;
                    if (isGenuine) {
                        resultDiv.innerHTML = '教育局反馈：证件信息真实有效。';
                        callback(true);
                        gameState.phoneConfirmedForged = false;
                    } else {
                        resultDiv.innerHTML = '教育局反馈：查无此人或证件不符，疑似伪造。';
                        callback(false);
                        gameState.phoneConfirmedForged = true;
                    }
                    setTimeout(() => {
                        modal.style.display = 'none';
                        confirmBtn.removeEventListener('click', onConfirm);
                        cancelBtn.removeEventListener('click', onCancel);
                        updateUI();
                    }, 2000);
                }, 1500);
            } else {
                resultDiv.innerHTML = '号码错误，无法核实。请查阅教育局电话簿。';
                resultDiv.style.color = '#ff8888';
                gameState.phoneConfirmedForged = false;
            }
        };
        
        const onCancel = () => {
            modal.style.display = 'none';
            confirmBtn.removeEventListener('click', onConfirm);
            cancelBtn.removeEventListener('click', onCancel);
            callback(false);
            gameState.phoneConfirmedForged = false;
            updateUI();
        };
        
        confirmBtn.addEventListener('click', onConfirm);
        cancelBtn.addEventListener('click', onCancel);
        if (!gameState.achievements.firstPhoneCall) unlockAchievement('firstPhoneCall', '第一次通话');
    }
}

function updatePhoneShortcuts() {
    const panel = document.getElementById('phone-shortcuts');
    if (gameState.upgrades.stickyNote && gameState.phoneNumbers) {
        panel.style.display = 'block';
        const btnContainer = document.getElementById('phone-buttons');
        btnContainer.innerHTML = '';
        const phones = [
            { label: '教育局核实', number: gameState.phoneNumbers.edu },
            { label: '实验中学王明校长', number: gameState.phoneNumbers.principal_sy },
            { label: '深圳中学李华校长', number: gameState.phoneNumbers.principal_sz },
            { label: '深圳高级中学张丽校长', number: gameState.phoneNumbers.principal_sg },
            { label: '深圳外国语学校陈芳校长', number: gameState.phoneNumbers.principal_wgy },
            { label: '教育局直属中学赵强校长', number: gameState.phoneNumbers.principal_jyj },
            { label: '纪检部举报', number: gameState.phoneNumbers.report }
        ];
        phones.forEach(p => {
            const btn = document.createElement('button');
            btn.innerText = p.label;
            btn.className = 'phone-btn';
            btn.onclick = () => {
                if (p.number === gameState.trainingPhoneNumber && !gameState.trainingCompleted && gameState.day === 1) {
                    showTrainingCall();
                } else if (gameState.currentVisitor) {
                    showPhoneShortcut(p.number, gameState.currentVisitor);
                } else {
                    showMessage('没有当前访客', '#ffaa00');
                }
            };
            btnContainer.appendChild(btn);
        });
    } else {
        panel.style.display = 'none';
    }
}

// ==================== 随机生成 ====================
function generateRandomName() {
    const surnames = ['陈', '李', '张', '刘', '王', '黄', '林', '周', '吴', '郑'];
    const names = ['明', '伟', '芳', '强', '敏', '静', '宇', '欣', '哲', '雨桐'];
    return surnames[Math.floor(Math.random() * surnames.length)] + 
           names[Math.floor(Math.random() * names.length)] +
           names[Math.floor(Math.random() * names.length)];
}

function randomDate(year) {
    const month = Math.floor(Math.random() * 12) + 1;
    const day = Math.floor(Math.random() * 28) + 1;
    return `${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
}

function randomExpiry() {
    const year = 2026 + Math.floor(Math.random() * 2);
    const month = Math.floor(Math.random() * 12) + 1;
    const day = Math.floor(Math.random() * 28) + 1;
    return `${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
}

function getExpectedStudentIdPrefix(grade) {
    if (grade === 7) return "2025";
    if (grade === 8) return "2024";
    return "2023";
}

function generateStudentId(grade, isForged) {
    const correctPrefix = getExpectedStudentIdPrefix(grade);
    let prefix = correctPrefix;
    if (isForged) {
        const yearNum = parseInt(correctPrefix);
        const options = [yearNum - 1, yearNum + 1];
        const fakeYear = options[Math.floor(Math.random() * options.length)];
        prefix = fakeYear.toString();
    }
    const suffix = Math.floor(Math.random() * 10000).toString().padStart(4, '0');
    return prefix + suffix;
}

function generateEscapeVisitor() {
    const school = SCHOOLS[Math.floor(Math.random() * SCHOOLS.length)];
    const grade = Math.floor(Math.random() * 3) + 7;
    let expectedBirthYear;
    if (grade === 7) expectedBirthYear = 2013;
    else if (grade === 8) expectedBirthYear = 2012;
    else expectedBirthYear = 2011;
    const birth = randomDate(expectedBirthYear);
    const studentId = generateStudentId(grade, false);
    const visitor = {
        name: generateRandomName(),
        grade: grade,
        birth: birth,
        studentId: studentId,
        expiry: randomExpiry(),
        school: school,
        isExperiment: (school === '深圳实验中学'),
        documents: ['studentCard'],
        forged: true,
        forgedDocs: ['studentCard'],
        healthStatus: '健康',
        transferLetter: null,
        purpose: null,
        isEscapeEvent: true,
        escapeMessage: "（他低声说：'检察员同学，我的证件是假的，但我可以帮你搞到逃跑所需的文件。如果你放我进去，我会报答你的。'）",
        isWanted: false
    };
    return visitor;
}

function generateNormalVisitor() {
    const school = SCHOOLS[Math.floor(Math.random() * SCHOOLS.length)];
    const isExperiment = (school === '深圳实验中学');
    const grade = Math.floor(Math.random() * 3) + 7;
    
    let correctBirthYear;
    if (grade === 7) correctBirthYear = 2013;
    else if (grade === 8) correctBirthYear = 2012;
    else correctBirthYear = 2011;
    let birthYear = correctBirthYear;
    let isBirthForged = false;
    if (Math.random() < 0.08) {
        const fakeYears = [2009, 2010, 2015, 2016, 2017];
        birthYear = fakeYears[Math.floor(Math.random() * fakeYears.length)];
        isBirthForged = true;
    }
    const birth = randomDate(birthYear);
    
    let isStudentIdForged = false;
    if (Math.random() < 0.08) isStudentIdForged = true;
    const studentId = generateStudentId(grade, isStudentIdForged);
    
    let visitor = {
        name: generateRandomName(),
        grade: grade,
        birth: birth,
        studentId: studentId,
        expiry: randomExpiry(),
        school: school,
        isExperiment: isExperiment,
        documents: ['studentCard'],
        forged: isBirthForged || isStudentIdForged,
        forgedDocs: [],
        healthStatus: '健康',
        transferLetter: null,
        purpose: null
    };
    if (isBirthForged) visitor.forgedDocs.push('birthDate');
    if (isStudentIdForged) visitor.forgedDocs.push('studentId');
    
    if (gameState.day >= 3) {
        if (isExperiment) {
            visitor.documents.push('campusCard');
            visitor.campusCard = { valid: Math.random() > 0.2, name: visitor.name };
        } else {
            visitor.documents.push('tempPass');
            visitor.tempPass = { validUntil: randomDate(2026), name: visitor.name };
        }
    }
    
    if (gameState.day >= 8 && !isExperiment) {
        visitor.documents.push('securityPass');
        const purposes = ['上课', '竞赛', '学生会交流', '图书馆', '社团活动', '转学'];
        visitor.securityPass = {
            studentId: visitor.studentId,
            name: visitor.name,
            school: visitor.school,
            purpose: purposes[Math.floor(Math.random() * purposes.length)]
        };
        visitor.purpose = visitor.securityPass.purpose;
    }
    
    if (gameState.day >= 15 && !isExperiment && visitor.purpose === '转学') {
        visitor.documents.push('transferLetter');
        visitor.transferLetter = {
            name: visitor.name,
            studentId: visitor.studentId,
            fromSchool: visitor.school,
            toSchool: '深圳实验中学',
            signatures: {
                fromPrincipal: visitor.school === '深圳实验中学' ? '王明' : '李国栋',
                toPrincipal: '王明'
            },
            forged: Math.random() < 0.3
        };
        if (visitor.transferLetter.forged) {
            visitor.forged = true;
            visitor.forgedDocs.push('transferLetter');
        }
    }
    
    if (gameState.day >= 20) {
        visitor.documents.push('healthCert');
        const healthOptions = ['健康', '健康', '健康', '健康', '感冒', '过敏'];
        visitor.healthStatus = healthOptions[Math.floor(Math.random() * healthOptions.length)];
        visitor.healthCert = {
            name: visitor.name,
            status: visitor.healthStatus,
            forged: (visitor.healthStatus !== '健康' && Math.random() < 0.5)
        };
        if (visitor.healthCert.forged) {
            visitor.forged = true;
            visitor.forgedDocs.push('healthCert');
        }
    }
    
    if (!visitor.forged && Math.random() < 0.1) {
        visitor.forged = true;
        visitor.forgedDocs.push('studentCard');
    }
    
    visitor.isWanted = checkIfWanted(visitor);
    return visitor;
}

function generateVisitor() {
    if (gameState.day === 25 && !gameState.day25EventTriggered && gameState.visitedToday === 0) {
        gameState.day25EventTriggered = true;
        return generateEscapeVisitor();
    }
    return generateNormalVisitor();
}

// ==================== 显示访客 ====================
function displayVisitor(visitor) {
    if (!visitor) return;
    document.getElementById('name').innerText = visitor.name;
    document.getElementById('grade').innerText = visitor.grade + '年级';
    document.getElementById('birth').innerText = visitor.birth;
    document.getElementById('student-id').innerText = visitor.studentId;
    document.getElementById('expiry').innerText = visitor.expiry;
    document.getElementById('school').innerText = visitor.school;
    
    const extraDiv = document.getElementById('extra-fields');
    extraDiv.innerHTML = '';
    if (visitor.campusCard) {
        extraDiv.innerHTML += `<div class="info-row compare-field" data-field="campusCard_valid"><span class="label">校园卡状态</span><span class="value">${visitor.campusCard.valid ? '有效' : '无效'}</span></div>`;
    }
    if (visitor.tempPass) {
        extraDiv.innerHTML += `<div class="info-row compare-field" data-field="tempPass_expiry"><span class="label">临时通行证有效期</span><span class="value">${visitor.tempPass.validUntil}</span></div>`;
    }
    if (visitor.securityPass) {
        extraDiv.innerHTML += `<div class="info-row compare-field" data-field="securityPass_purpose"><span class="label">纪检部准入证目的</span><span class="value">${visitor.securityPass.purpose}</span></div>`;
    }
    if (visitor.transferLetter) {
        const forgedMark = visitor.transferLetter.forged ? ' (可疑)' : '';
        extraDiv.innerHTML += `<div class="info-row compare-field" data-field="transferLetter_from"><span class="label">转出学校</span><span class="value">${visitor.transferLetter.fromSchool}</span></div>`;
        extraDiv.innerHTML += `<div class="info-row compare-field" data-field="transferLetter_to"><span class="label">转入学校</span><span class="value">${visitor.transferLetter.toSchool}</span></div>`;
        extraDiv.innerHTML += `<div class="info-row compare-field" data-field="transferLetter_signature"><span class="label">签字情况</span><span class="value">${forgedMark || '正常'}</span></div>`;
        if (gameState.day >= 20) {
            extraDiv.innerHTML += `<div class="info-row"><span class="label"></span><span class="value"><button id="confiscate-letter-btn" class="action confiscate" style="background:#a57c2a; padding:4px 8px;">没收介绍信</button></span></div>`;
        }
    }
    if (visitor.healthCert) {
        extraDiv.innerHTML += `<div class="info-row compare-field" data-field="healthCert_status"><span class="label">健康状况</span><span class="value">${visitor.healthCert.status}${visitor.healthCert.forged ? ' (可疑)' : ''}</span></div>`;
    }
    
    document.querySelectorAll('.compare-field').forEach(field => {
        field.style.cursor = gameState.compareMode ? 'pointer' : 'default';
        let labelElem = field.querySelector('.label');
        let valueElem = field.querySelector('.value');
        if (!labelElem || !valueElem) return;
        const label = labelElem.innerText;
        const value = valueElem.innerText;
        field.onclick = () => handleCompareFieldClick(field, label, value);
    });
    
    const currentDateField = document.getElementById('current-date-bar');
    if (currentDateField) {
        currentDateField.style.cursor = gameState.compareMode ? 'pointer' : 'default';
        const label = currentDateField.querySelector('.label').innerText;
        const value = currentDateField.querySelector('.value').innerText;
        currentDateField.onclick = () => handleCompareFieldClick(currentDateField, label, value);
    }
    
    let dialogue = `学生: "检察员同学，我是${visitor.school}的${visitor.name}，来参加活动。"`;
    if (visitor.purpose && visitor.purpose !== '上课') {
        dialogue = `学生: "检察员同学，我是${visitor.school}的${visitor.name}，来${visitor.purpose}。"`;
    }
    if (visitor.isEscapeEvent) {
        dialogue = `学生: "检察员同学，我... (他显得非常紧张) ${visitor.escapeMessage}"`;
    }
    if (visitor.isWanted) {
        dialogue = `学生: "检察员同学... (他眼神躲闪) 我是${visitor.school}的${visitor.name}..." 系统提示: ⚠️ 该生涉嫌违纪，请立即处理！`;
    }
    document.getElementById('visitor-dialogue').innerHTML = dialogue;
    
    document.getElementById('card-status').innerHTML = '';
    
    // 没收按钮事件
    const confiscateLetterBtn = document.getElementById('confiscate-letter-btn');
    if (confiscateLetterBtn) {
        confiscateLetterBtn.onclick = (e) => {
            e.stopPropagation();
            if (!gameState.canCheck) return;
            gameState.canCheck = false;
            disableActionButtons();
            if (gameState.day < 20) {
                showMessage('没收功能尚未启用（第20天起）', '#ffaa00');
                gameState.canCheck = true;
                enableActionButtons();
                return;
            }
            if (!visitor.transferLetter) {
                showMessage('没有可没收的介绍信', '#ffaa00');
                gameState.canCheck = true;
                enableActionButtons();
                return;
            }
            if (visitor.transferLetter.forged) {
                visitor.transferLetter = null;
                visitor.forgedDocs = visitor.forgedDocs.filter(d => d !== 'transferLetter');
                visitor.forged = visitor.forgedDocs.length > 0;
                showMessage(`已没收伪造的转学介绍信。`, '#88aa88');
            } else {
                if (gameState.money >= 25) {
                    gameState.money -= 25;
                    gameState.confiscatedNormalLetters++;
                    visitor.transferLetter = null;
                    visitor.documents = visitor.documents.filter(d => d !== 'transferLetter');
                    showMessage(`没收了正常的转学介绍信，罚款25元。已记录没收正常介绍信次数：${gameState.confiscatedNormalLetters}`, '#ffaa88');
                    if (gameState.confiscatedNormalLetters === 1 && !gameState.achievements.confiscator) {
                        unlockAchievement('confiscator', '铁面无私（没收正常介绍信）');
                    }
                } else {
                    showMessage('金钱不足25元，无法没收。', '#ff8888');
                    gameState.canCheck = true;
                    enableActionButtons();
                    return;
                }
            }
            updateUI();
            displayVisitor(visitor);
            showNextButton();
        };
    }
}

// ==================== 对比逻辑 ====================
function enterCompareMode() {
    gameState.compareMode = true;
    gameState.compareFirstField = null;
    showMessage('对比模式已激活，请点击第一个字段', '#ffffa0');
    document.querySelectorAll('.compare-field').forEach(field => {
        field.style.cursor = 'pointer';
        field.style.backgroundColor = '#e0e8c0';
    });
    if (gameState.talent === 'insight' && !gameState.compareUsed) {
        gameState.compareUsed = true;
        showMessage('天赋洞察力生效：本次对比不消耗时间', '#88ff88', 3000);
    }
}

function exitCompareMode() {
    gameState.compareMode = false;
    gameState.compareFirstField = null;
    document.querySelectorAll('.compare-field').forEach(field => {
        field.style.cursor = 'default';
        field.style.backgroundColor = '';
        field.classList.remove('compare-selected');
    });
}

function extractGradeNumber(gradeStr) {
    const match = gradeStr.match(/[七八九]年级/);
    if (!match) return null;
    const ch = match[0][0];
    if (ch === '七') return 7;
    if (ch === '八') return 8;
    if (ch === '九') return 9;
    return null;
}

function isDateString(str) {
    return /^\d{4}-\d{2}-\d{2}$/.test(str);
}

function smartCompare(field1, field2, value1, value2) {
    const label1 = field1.label;
    const label2 = field2.label;
    
    if ((label1.includes('年级') && label2.includes('出生日期')) || 
        (label1.includes('出生日期') && label2.includes('年级'))) {
        const gradeVal = label1.includes('年级') ? value1 : value2;
        const birthVal = label1.includes('出生日期') ? value1 : value2;
        const gradeNum = extractGradeNumber(gradeVal);
        const birthYear = parseInt(birthVal.split('-')[0]);
        let expectedYear = null;
        if (gradeNum === 7) expectedYear = 2013;
        else if (gradeNum === 8) expectedYear = 2012;
        else if (gradeNum === 9) expectedYear = 2011;
        if (expectedYear !== null && !isNaN(birthYear)) {
            const isMatch = (birthYear === expectedYear);
            return { isMatch, message: `出生年份${isMatch ? '匹配' : '不匹配'}年级（应为${expectedYear}年）` };
        } else {
            return { isMatch: false, message: '无法解析年级或出生日期' };
        }
    }
    
    if (isDateString(value1) && isDateString(value2)) {
        const date1 = new Date(value1);
        const date2 = new Date(value2);
        if (date1 < date2) {
            return { isMatch: false, message: `${value1} 早于 ${value2}` };
        } else if (date1 > date2) {
            return { isMatch: false, message: `${value1} 晚于 ${value2}` };
        } else {
            return { isMatch: true, message: `日期相同 (${value1})` };
        }
    }
    
    const isMatch = (value1 === value2);
    if (isMatch) {
        return { isMatch: true, message: `内容一致: ${value1}` };
    } else {
        return { isMatch: false, message: `"${value1}" ≠ "${value2}"` };
    }
}

function handleCompareFieldClick(element, fieldLabel, fieldValue) {
    if (!gameState.compareMode) return;
    if (!gameState.compareFirstField) {
        gameState.compareFirstField = { element, label: fieldLabel, value: fieldValue };
        element.classList.add('compare-selected');
        showMessage(`已选: ${fieldLabel} = ${fieldValue}，请点击第二个字段`, '#ffffa0');
    } else {
        const first = gameState.compareFirstField;
        const second = { element, label: fieldLabel, value: fieldValue };
        const result = smartCompare(first, second, first.value, second.value);
        if (result.isMatch) {
            showMessage(`✅ 比对结果: ${result.message}`, '#88ff88');
        } else {
            showMessage(`❌ 比对结果: ${result.message}`, '#ff8888');
        }
        first.element.classList.remove('compare-selected');
        exitCompareMode();
    }
}

// ==================== 手动喊下一位 ====================
function showNextButton() {
    const nextBtn = document.getElementById('btn-next-student');
    if (nextBtn) nextBtn.style.display = 'inline-block';
}

function hideNextButton() {
    const nextBtn = document.getElementById('btn-next-student');
    if (nextBtn) nextBtn.style.display = 'none';
}

function callNextStudent() {
    hideNextButton();
    gameState.canCheck = true;
    enableActionButtons();
    if (gameState.visitedToday < gameState.totalVisitorsToday) {
        nextVisitor();
    } else {
        endDay();
    }
}

// ==================== 贿赂事件 ====================
function showBribeOption(visitor) {
    const modal = document.getElementById('event-modal');
    document.getElementById('event-title').innerText = '💰 贿赂事件';
    document.getElementById('event-desc').innerHTML = `
        <p>该学生试图向你行贿！</p>
        <p><strong>学生 ${visitor.name}</strong> 低声说：“检察员同学，请高抬贵手，这是一点心意……”</p>
        <p>他递给你 20 元。</p>
        <p style="color: #aa4444; font-size: 12px;">⚠️ 接受贿赂可能影响结局</p>
    `;
    const optionsDiv = document.getElementById('event-options');
    optionsDiv.innerHTML = '';
    
    const acceptBtn = document.createElement('button');
    acceptBtn.innerText = '💰 接受贿赂 (+20元)';
    acceptBtn.onclick = () => {
        gameState.money += 20;
        gameState.corruption++;
        if (gameState.corruption === 1 && !gameState.achievements.corrupt) {
            unlockAchievement('corrupt', '腐败的检察员');
        }
        showMessage('你收下了贿赂，金钱+20元。', '#ffaa00', 2000);
        gameState.visitedToday++;
        updateUI();
        modal.style.display = 'none';
        showNextButton();
    };
    optionsDiv.appendChild(acceptBtn);
    
    const rejectBtn = document.createElement('button');
    rejectBtn.innerText = '🚫 拒绝贿赂 (正常扣分)';
    rejectBtn.onclick = () => {
        showMessage('你拒绝了贿赂，坚持原则。', '#88aa88', 2000);
        let penalty = 10;
        gameState.money -= penalty;
        gameState.visitedToday++;
        updateUI();
        modal.style.display = 'none';
        showNextButton();
    };
    optionsDiv.appendChild(rejectBtn);
    
    if (visitor.forged) {
        const arrestBtn = document.createElement('button');
        arrestBtn.innerText = '🚔 逮捕 (获得嘉奖+20元)';
        arrestBtn.onclick = () => {
            gameState.money += 20;
            showMessage('你逮捕了该学生，获得嘉奖+20元。', '#88aa88', 2000);
            gameState.visitedToday++;
            updateUI();
            modal.style.display = 'none';
            showNextButton();
            if (!gameState.achievements.firstArrest) unlockAchievement('firstArrest', '执法如山');
        };
        optionsDiv.appendChild(arrestBtn);
    }
    
    modal.style.display = 'flex';
}

// ==================== 核心判定逻辑 ====================
function checkVisitor(visitor, approved) {
    if (!gameState.canCheck) return;
    gameState.canCheck = false;
    disableActionButtons();

    if (!gameState.trainingCompleted && gameState.day === 1) {
        showMessage('请先完成新人培训（拨打纪检部培训电话）', '#ffaa00');
        gameState.canCheck = true;
        enableActionButtons();
        return;
    }
    if (gameState.phoneCallActive) {
        showMessage('请先完成电话核实', '#ffaa00');
        gameState.canCheck = true;
        enableActionButtons();
        return;
    }
    
    if (visitor.isEscapeEvent) {
        if (approved) {
            gameState.money -= 50;
            showMessage('[特殊事件] 你放走了逃跑者，被罚款50元。他感激地看了你一眼，并低声说：“我会帮你搞到逃跑文件的。”', '#ffaa88', 3000);
            gameState.escapeReady = true;
            gameState.visitedToday++;
            updateUI();
            showNextButton();
            return;
        } else {
            showMessage('[特殊事件] 你拒绝了逃跑者，他沮丧地离开了。', '#cccccc', 2000);
            gameState.visitedToday++;
            updateUI();
            showNextButton();
            return;
        }
    }
    
    if (visitor.isWanted && approved) {
        gameState.money -= 100;
        showMessage('[通缉犯] 你放走了通缉犯！被罚款100元！', '#ff4444');
        gameState.visitedToday++;
        updateUI();
        showNextButton();
        return;
    }
    
    let shouldAllow = true;
    let reason = '';
    
    if (!visitor.studentId || visitor.expiry < new Date().toISOString().slice(0,10)) {
        shouldAllow = false;
        reason = '学生证过期或无效';
    }
    if (visitor.campusCard && !visitor.campusCard.valid) {
        shouldAllow = false;
        reason = '校园卡无效';
    }
    if (visitor.tempPass && visitor.tempPass.validUntil < new Date().toISOString().slice(0,10)) {
        shouldAllow = false;
        reason = '临时通行证过期';
    }
    if (visitor.securityPass && !visitor.securityPass.purpose) {
        shouldAllow = false;
        reason = '准入证目的不明';
    }
    if (visitor.transferLetter) {
        if (visitor.transferLetter.forged) {
            shouldAllow = false;
            reason = '转学介绍信疑似伪造';
        }
        const fromPrincipal = visitor.transferLetter.fromSchool === '深圳实验中学' ? '王明' : '李国栋';
        if (visitor.transferLetter.signatures.fromPrincipal !== fromPrincipal) {
            shouldAllow = false;
            reason = '转学介绍信签名不符';
        }
    }
    if (visitor.healthCert) {
        if (visitor.healthCert.status !== '健康') {
            shouldAllow = false;
            reason = '健康状况不符合要求';
        }
        if (visitor.healthCert.forged) {
            shouldAllow = false;
            reason = '健康证明伪造';
        }
    }
    
    let expectedBirthYear;
    if (visitor.grade === 7) expectedBirthYear = 2013;
    else if (visitor.grade === 8) expectedBirthYear = 2012;
    else expectedBirthYear = 2011;
    const birthYear = parseInt(visitor.birth.split('-')[0]);
    if (birthYear !== expectedBirthYear) {
        shouldAllow = false;
        reason = `出生日期与年级不符（应为${expectedBirthYear}年）`;
    }
    
    const expectedPrefix = getExpectedStudentIdPrefix(visitor.grade);
    const actualPrefix = visitor.studentId.substring(0, 4);
    if (actualPrefix !== expectedPrefix) {
        shouldAllow = false;
        reason = `学号前缀不符（应为${expectedPrefix}开头）`;
    }
    
    const isCorrect = (approved === shouldAllow);
    
    if (isCorrect) {
        let reward = gameState.simpleMode ? 10 : 5;
        if (gameState.talent === 'justice') reward += 5;
        gameState.money += reward;
        gameState.totalEarned += reward;
        gameState.correctCount++;
        showMessage(`[正确] 审核正确 +${reward}元`, '#2c7a2c');
        if (gameState.correctCount === 10 && !gameState.achievements.firstTenCorrect) unlockAchievement('firstTenCorrect', '十连正确');
        if (gameState.totalEarned >= 1000 && !gameState.achievements.millionaire) unlockAchievement('millionaire', '万元户');
        gameState.visitedToday++;
        updateUI();
        showNextButton();
    } else {
        const bribeChance = 0.30;
        if (visitor.forged && Math.random() < bribeChance) {
            showBribeOption(visitor);
            return;
        } else {
            let penalty = 10;
            gameState.money -= penalty;
            showMessage(`[错误] 审核错误 -${penalty}元，原因: ${reason}`, '#9b4a2a');
            gameState.visitedToday++;
            updateUI();
            showNextButton();
        }
    }
}

function arrestVisitor() {
    if (!gameState.canCheck) return;
    gameState.canCheck = false;
    disableActionButtons();

    if (!gameState.trainingCompleted && gameState.day === 1) {
        showMessage('请先完成新人培训（拨打纪检部培训电话）', '#ffaa00');
        gameState.canCheck = true;
        enableActionButtons();
        return;
    }
    if (!gameState.currentVisitor || !gameState.currentVisitor.forged) {
        showMessage('当前访客无可疑文件，不能逮捕', '#ffaa00');
        gameState.canCheck = true;
        enableActionButtons();
        return;
    }
    if (gameState.currentVisitor.isEscapeEvent) {
        showMessage('[逮捕] 你逮捕了逃跑者，他绝望地低下了头。获得嘉奖 +20元', '#88aa88');
        gameState.money += 20;
        gameState.visitedToday++;
        updateUI();
        showNextButton();
        return;
    }
    let arrestBonus = 20;
    if (gameState.talent === 'justice') arrestBonus += 10;
    gameState.money += arrestBonus;
    showMessage(`[逮捕] 已逮捕伪造者，获得嘉奖 +${arrestBonus}元`, '#88aa88');
    gameState.visitedToday++;
    updateUI();
    showNextButton();
    if (!gameState.achievements.firstArrest) unlockAchievement('firstArrest', '执法如山');
}

function confiscateItem() {
    showMessage('请使用证件上的“没收介绍信”按钮。', '#ffaa00');
}

function updateConfiscatedList() {
    const listDiv = document.getElementById('confiscated-list');
    listDiv.innerHTML = '';
    if (gameState.confiscatedItems.length === 0) {
        listDiv.innerHTML = '<div>暂无没收物品</div>';
        return;
    }
    gameState.confiscatedItems.forEach((item, idx) => {
        const div = document.createElement('div');
        div.innerText = `第${item.day}天 没收 ${item.name} (${item.school}) 伪造介绍信`;
        listDiv.appendChild(div);
    });
}

// ==================== 逃亡计划触发函数 ====================
function triggerEscapeEnding() {
    if (gameState.timerInterval) clearInterval(gameState.timerInterval);
    showEnding('逃亡结局', '你带着匆匆伪造的证件和车票离开了深圳，8小时后，浑身酸痛的你看到了你的新学校：河北衡水第二中，有些迟疑的学生会干部批准你进入，现在喘口气吧。但是记住：“衡水二中至高无上！”', {
        money: Math.floor(gameState.money),
        day: gameState.day,
        correct: gameState.correctCount
    });
    unlockAchievement('fugitive', '逃亡者');
}

// ==================== 结局对话框 ====================
function showEnding(title, description, details = {}) {
    const modal = document.getElementById('ending-modal');
    const titleElem = document.getElementById('ending-title');
    const descElem = document.getElementById('ending-desc');
    const date = new Date().toLocaleString();
    const seal = "═════════════════════════════\n          [ 绝密 ]\n═════════════════════════════";
    const signature = "校园安全部 签发\n部长 李建国 (印)";
    let fullDesc = `${seal}\n\n档案编号: ${Math.floor(Math.random()*100000)}\n日期: ${date}\n\n${description}\n\n${signature}`;
    if (details.money !== undefined) fullDesc += `\n\n最终余额: ${details.money} 元`;
    if (details.day !== undefined) fullDesc += `\n执勤天数: ${details.day} 天`;
    if (details.correct !== undefined) fullDesc += `\n正确审核: ${details.correct} 次`;
    titleElem.innerText = `「 ${title} 」`;
    descElem.innerText = fullDesc;
    modal.style.display = 'flex';
    const restartBtn = document.getElementById('restart-from-ending');
    const handler = () => {
        modal.style.display = 'none';
        location.reload();
    };
    restartBtn.onclick = handler;
}

function endGame() {
    if (gameState.timerInterval) clearInterval(gameState.timerInterval);
    let endingTitle = '', endingDesc = '';
    let details = {
        money: Math.floor(gameState.money),
        day: gameState.day,
        correct: gameState.correctCount
    };
    
    if (gameState.corruption >= 3) {
        endingTitle = '腐败结局';
        endingDesc = '你因多次收受贿赂被纪检部调查，最终被开除并移交司法机关。你的名字被永久从学校名册中删除。';
        showEnding(endingTitle, endingDesc, details);
        return;
    }
    
    if (gameState.escapeReady) {
        endingTitle = '逃亡结局';
        endingDesc = '你带着匆匆伪造的证件和车票离开了深圳，8小时后，浑身酸痛的你看到了你的新学校：河北衡水第二中，有些迟疑的学生会干部批准你进入，现在喘口气吧。但是记住：“衡水二中至高无上！”';
        unlockAchievement('fugitive', '逃亡者');
    } else if (gameState.helpCount >= 5) {
        endingTitle = '革命线结局';
        endingDesc = '同志，您好！今天是光荣的一天！学生斗争委员会的革命成功了！现在我们推行了民主改革，您被任命为新一届学生会纪检部部长。校园里充满了希望，但请您明白，这条路充满挑战。现在，光荣属于新深圳实验！';
        unlockAchievement('revolutionary', '革命先驱');
    } else if (gameState.helpCount > 0) {
        endingTitle = '忠诚线结局（枪毙）';
        endingDesc = '同学你好，校园安全部对你的政治和工作情况进行了审查，经查，你与非法组织有联系，犯有颠覆学校罪。纪检部和光荣的深圳实验不会容忍背叛，所以你被除名了，工作将由新人接替，现在和我们走一趟吧。';
        unlockAchievement('loyalist', '忠诚卫士');
    } else {
        endingTitle = '忠诚线结局（平稳）';
        endingDesc = '“同志，您好。很高兴地通知你，你的政治审核通过，可以继续担任纪检部科员，所以松口气吧。我们和深中人达成了新协议，4月1号返回你的工作岗位，祝好运！以及，光荣属于深圳实验！”';
        unlockAchievement('loyalist', '忠诚卫士');
    }
    if (gameState.money >= 1000) unlockAchievement('millionaire', '万元户');
    if (gameState.stockProfit >= 500) unlockAchievement('stockMaster', '股神');
    if (gameState.helpCount >= 5) unlockAchievement('undercover', '地下工作者');
    if (gameState.day >= 30) unlockAchievement('survivalist', '老油条');
    if (gameState.achievements.perfectDay) unlockAchievement('perfectDay', '完美执勤');
    
    showEnding(endingTitle, endingDesc, details);
}

function debtEnding() {
    if (gameState.timerInterval) clearInterval(gameState.timerInterval);
    showEnding('负债结局', '由于长期负债，你被纪检部隔离审查，最终失去了学生身份...', { money: Math.floor(gameState.money), day: gameState.day });
}

// ==================== 升级系统 ====================
function renderUpgradePanel() {
    const panel = document.getElementById('upgrade-list');
    panel.innerHTML = '';
    const upgrades = [
        { id: 'quickBookmarks', name: '快捷收藏夹', price: 20, desc: '网站直接显示在桌面' },
        { id: 'advancedDorm', name: '高级宿舍', price: 100, desc: '免房租水电' },
        { id: 'stickyNote', name: '便签', price: 40, desc: '一键拨打常用电话' },
        { id: 'autoTrade', name: '一键填写交割单', price: 30, desc: '股票交易自动填价' }
    ];
    upgrades.forEach(up => {
        if (!gameState.upgrades[up.id]) {
            const btn = document.createElement('button');
            btn.innerText = `${up.name} - ${up.price}元`;
            btn.onclick = () => {
                if (gameState.money >= up.price) {
                    gameState.money -= up.price;
                    gameState.upgrades[up.id] = true;
                    updateUI();
                    applyUpgradeEffect(up.id);
                } else {
                    showMessage('钱不够！', 'red');
                }
            };
            panel.appendChild(btn);
        }
    });
}

function applyUpgradeEffect(upgradeId) {
    if (upgradeId === 'quickBookmarks') {
        showMessage('快捷收藏夹已激活，网站常驻桌面', 'green');
        updateBrowserAccess();
    }
    if (upgradeId === 'stickyNote') {
        showMessage('便签已购买，快捷电话面板已启用', 'green');
        updatePhoneShortcuts();
    }
    if (upgradeId === 'autoTrade') {
        showMessage('一键填写交割单已激活，交易时自动填入价格', 'green');
    }
}

// ==================== 成就界面 ====================
function showAchievements() {
    const modal = document.getElementById('achievements-modal');
    const listDiv = document.getElementById('achievements-list');
    const achievementsMap = {
        firstArrest: { name: '执法如山', desc: '首次逮捕伪造者' },
        firstPhoneCall: { name: '第一次通话', desc: '首次使用电话核实' },
        firstStockTrade: { name: '初入股市', desc: '首次进行股票交易' },
        firstHelpOrganization: { name: '暗中支持', desc: '首次帮助学生斗争委员会' },
        firstConfiscation: { name: '铁面无私', desc: '首次没收伪造介绍信' },
        firstTenCorrect: { name: '十连正确', desc: '累计正确审核10次' },
        millionaire: { name: '万元户', desc: '累计赚取1000元' },
        perfectDay: { name: '完美执勤', desc: '某天全部审核正确' },
        stockMaster: { name: '股神', desc: '股票盈利超过500元' },
        undercover: { name: '地下工作者', desc: '帮助学生组织5次以上' },
        whistleblower: { name: '举报者', desc: '举报组织3次以上' },
        survivalist: { name: '老油条', desc: '存活30天' },
        fugitive: { name: '逃亡者', desc: '触发逃亡结局' },
        revolutionary: { name: '革命先驱', desc: '触发革命结局' },
        loyalist: { name: '忠诚卫士', desc: '触发忠诚结局' },
        confiscator: { name: '铁面无私·改', desc: '没收正常介绍信' },
        corrupt: { name: '腐败的检察员', desc: '第一次收受贿赂' }
    };
    listDiv.innerHTML = '';
    for (const [key, ach] of Object.entries(achievementsMap)) {
        const unlocked = gameState.achievements[key] || false;
        const div = document.createElement('div');
        div.className = 'achievement-item';
        div.innerHTML = `
            <div class="${unlocked ? 'achievement-unlocked' : 'achievement-locked'}">
                ${unlocked ? '✅' : '🔒'} <strong>${ach.name}</strong><br>
                <span style="font-size: 11px;">${ach.desc}</span>
            </div>
        `;
        listDiv.appendChild(div);
    }
    modal.style.display = 'flex';
}

// ==================== 每日流程 ====================
function startNewDay() {
    gameState.canCheck = true;
    enableActionButtons();
    hideNextButton();
    
    let cost = 0;
    if (!gameState.upgrades.advancedDorm) {
        cost = 10 + 20;
        if (gameState.talent === 'economic') cost = Math.floor(cost / 2);
        gameState.money -= cost;
        showMessage(`扣除房租水电: -${cost}元`, '#cc8888');
    } else {
        showMessage('高级宿舍生效，免房租水电！', '#88aa88');
    }
    
    if (gameState.simpleMode) {
        let bonus = 20;
        if (gameState.talent === 'economic') bonus += 10;
        gameState.money += bonus;
        showMessage(`简单模式每日补贴 +${bonus}元`, '#88aa88');
    }
    
    if (gameState.day === 1 && gameState.money < 0) {
        gameState.money = 0;
        showMessage('第一天学校提供了临时补助，你的金钱已归零。', '#ffaa88');
    }
    
    if (gameState.money < 0) {
        debtEnding();
        return;
    }
    
    updateStockPrices();
    gameState.wantedList = generateWantedList();
    gameState.totalVisitorsToday = Math.min(10 + Math.floor(gameState.day / 5), 20);
    gameState.visitedToday = 0;
    
    const nextDate = new Date(gameState.gameDate);
    nextDate.setDate(gameState.gameDate.getDate() + 1);
    gameState.gameDate = nextDate;
    updateDateDisplay();
    
    sendDailyMail();
    checkOrganizationEvents();
    triggerFlavorEvent();
    
    if (gameState.day === 1 && !gameState.trainingCompleted && !gameState.tutorialShown) {
        gameState.tutorialShown = true;
        showNote(() => {
            proceedWithNewspaper();
        });
    } else {
        proceedWithNewspaper();
    }
    
    function proceedWithNewspaper() {
        if (!gameState.newspaperShownToday) {
            showNewspaper(() => {
                gameState.newspaperShownToday = true;
                gameState.currentVisitor = generateVisitor();
                displayVisitor(gameState.currentVisitor);
                gameState.visitedToday++;
                updateUI();
                if (gameState.timerInterval) clearInterval(gameState.timerInterval);
                gameState.timeLeft = 300;
                gameState.timerInterval = setInterval(() => {
                    if (gameState.timeLeft <= 1) {
                        clearInterval(gameState.timerInterval);
                        endDay();
                    } else {
                        gameState.timeLeft--;
                        document.getElementById('time-left').innerText = formatTime(gameState.timeLeft);
                    }
                }, 1000);
            });
        } else {
            gameState.currentVisitor = generateVisitor();
            displayVisitor(gameState.currentVisitor);
            gameState.visitedToday++;
            updateUI();
            if (gameState.timerInterval) clearInterval(gameState.timerInterval);
            gameState.timeLeft = 300;
            gameState.timerInterval = setInterval(() => {
                if (gameState.timeLeft <= 1) {
                    clearInterval(gameState.timerInterval);
                    endDay();
                } else {
                    gameState.timeLeft--;
                    document.getElementById('time-left').innerText = formatTime(gameState.timeLeft);
                }
            }, 1000);
        }
    }
    
    if (gameState.escapeReady && gameState.confiscatedNormalLetters >= 1 && gameState.money >= 300) {
        let escapeBtn = document.getElementById('escape-plan-btn');
        if (!escapeBtn) {
            escapeBtn = document.createElement('button');
            escapeBtn.id = 'escape-plan-btn';
            escapeBtn.innerText = '🏃 启动逃亡计划';
            escapeBtn.className = 'small-btn';
            escapeBtn.style.background = '#8a4a2a';
            escapeBtn.onclick = () => {
                if (confirm('确定要启动逃亡计划吗？你将立刻结束游戏并进入逃亡结局。')) {
                    triggerEscapeEnding();
                }
            };
            document.getElementById('status-bar').appendChild(escapeBtn);
        }
    } else {
        const escapeBtn = document.getElementById('escape-plan-btn');
        if (escapeBtn) escapeBtn.remove();
    }
}

function nextVisitor() {
    if (gameState.visitedToday < gameState.totalVisitorsToday) {
        gameState.currentVisitor = generateVisitor();
        displayVisitor(gameState.currentVisitor);
        gameState.visitedToday++;
        gameState.phoneConfirmedForged = false;
        updateUI();
        gameState.canCheck = true;
        enableActionButtons();
        hideNextButton();
    } else {
        endDay();
    }
}

function endDay() {
    if (gameState.timerInterval) clearInterval(gameState.timerInterval);
    if (gameState.visitedToday === gameState.totalVisitorsToday && gameState.correctCount === gameState.totalVisitorsToday) {
        if (!gameState.achievements.perfectDay) {
            gameState.achievements.perfectDay = true;
            showMessage('🏆 成就解锁：完美执勤（当天全部审核正确）', '#ffcc00', 4000);
        }
    }
    if (gameState.day >= 30) {
        endGame();
        return;
    }
    gameState.day++;
    gameState.newspaperShownToday = false;
    startNewDay();
}

// ==================== 电脑/电话查询 ====================
function initComputer() {
    function bindBookmarkEvents() {
        document.querySelectorAll('.bookmark').forEach(btn => {
            if (btn.hasListener) return;
            btn.addEventListener('click', (e) => {
                const site = btn.dataset.site;
                let content = '';
                if (site === 'schools') {
                    if (gameState.phoneNumbers) {
                        content = '<strong>深圳各中学信息</strong><br>' +
                            '深圳实验中学: 校长 王明，电话 ' + gameState.phoneNumbers.principal_sy + '<br>' +
                            '深圳中学: 校长 李华，电话 ' + gameState.phoneNumbers.principal_sz + '<br>' +
                            '深圳高级中学: 校长 张丽，电话 ' + gameState.phoneNumbers.principal_sg + '<br>' +
                            '深圳外国语学校: 校长 陈芳，电话 ' + gameState.phoneNumbers.principal_wgy + '<br>' +
                            '教育局直属中学: 校长 赵强，电话 ' + gameState.phoneNumbers.principal_jyj;
                    } else {
                        content = '<strong>深圳各中学信息</strong><br>暂无电话数据';
                    }
                } else if (site === 'phone') {
                    if (gameState.phoneNumbers) {
                        content = '教育局核实电话: ' + gameState.phoneNumbers.edu + '<br>纪检部监督: ' + gameState.phoneNumbers.report;
                    } else {
                        content = '教育局核实电话: 暂无<br>纪检部监督: 暂无';
                    }
                } else if (site === 'rules') {
                    content = '准入规定:<br>' +
                        '1. 学生证需在有效期内<br>' +
                        '2. 第3天起，实验学生须出示有效校园卡，外校学生须出示临时通行证<br>' +
                        '3. 第8天起，外校学生须出示纪检部准入证并说明目的<br>' +
                        '4. 第15天起，转学目的需提供转学介绍信（须双方校长签字）<br>' +
                        '5. 第20天起，所有人需提供健康证明（仅健康状态允许）<br>' +
                        '6. 伪造文件将没收并可能逮捕<br>' +
                        '7. 注意核对出生日期是否与年级匹配（七年级≈2013年出生）<br>' +
                        '8. 学号前缀应与入学年份匹配（七年级2025，八年级2024，九年级2023）';
                } else if (site === 'wanted') {
                    if (gameState.wantedList && gameState.wantedList.length > 0) {
                        content = '<strong>通缉令</strong><br>';
                        gameState.wantedList.forEach(w => {
                            content += `姓名: ${w.name}，学号: ${w.studentId}<br>`;
                        });
                    } else {
                        content = '当前协查通报: 暂无通缉犯。';
                    }
                }
                document.getElementById('web-content').innerHTML = content;
            });
            btn.hasListener = true;
        });
    }
    
    bindBookmarkEvents();
    
    const bookmarksDiv = document.getElementById('bookmarks');
    const existingPhoneBtn = document.getElementById('custom-phone-btn');
    if (!existingPhoneBtn) {
        const phoneBtn = document.createElement('button');
        phoneBtn.id = 'custom-phone-btn';
        phoneBtn.innerText = '电话核实（整容/身份）';
        phoneBtn.classList.add('bookmark');
        phoneBtn.onclick = () => {
            if (gameState.currentVisitor) {
                showPhoneInputModal(gameState.currentVisitor, (isGenuine) => {
                    if (isGenuine) {
                        showMessage('电话核实：证件真实有效', '#88aa88');
                    } else {
                        showMessage('电话核实：证件疑似伪造，请拒绝进入', '#ff8888');
                        gameState.currentVisitor.forged = true;
                    }
                    displayVisitor(gameState.currentVisitor);
                    updateUI();
                });
            } else {
                showMessage('没有当前访客', '#ffaa00');
            }
        };
        bookmarksDiv.appendChild(phoneBtn);
    }
    
    if (!gameState.trainingCompleted && gameState.day === 1 && !document.getElementById('training-btn')) {
        const trainingBtn = document.createElement('button');
        trainingBtn.id = 'training-btn';
        trainingBtn.innerText = '📞 新人培训 (0755-00000000)';
        trainingBtn.classList.add('bookmark');
        trainingBtn.style.background = '#8a4a2a';
        trainingBtn.onclick = () => {
            showTrainingCall();
        };
        bookmarksDiv.appendChild(trainingBtn);
    }
    
    const openBrowserBtn = document.getElementById('open-browser-btn');
    if (openBrowserBtn) {
        openBrowserBtn.onclick = () => {
            document.getElementById('browser-unlock').style.display = 'none';
            document.getElementById('browser-content').style.display = 'block';
            bindBookmarkEvents();
            if (!gameState.trainingCompleted && gameState.day === 1 && !document.getElementById('training-btn')) {
                const newTrainingBtn = document.createElement('button');
                newTrainingBtn.id = 'training-btn';
                newTrainingBtn.innerText = '📞 新人培训 (0755-00000000)';
                newTrainingBtn.classList.add('bookmark');
                newTrainingBtn.style.background = '#8a4a2a';
                newTrainingBtn.onclick = () => { showTrainingCall(); };
                document.getElementById('bookmarks').appendChild(newTrainingBtn);
            }
        };
    }
    
    const mailboxBtn = document.getElementById('mailbox-btn');
    if (mailboxBtn) {
        mailboxBtn.onclick = openMailbox;
    }
    
    const achievementsBtn = document.getElementById('achievements-btn');
    if (achievementsBtn) {
        achievementsBtn.onclick = showAchievements;
    }
    
    const tradeBtn = document.getElementById('trade-submit');
    if (tradeBtn) tradeBtn.onclick = executeTrade;
    const upgradeAutoBtn = document.getElementById('upgrade-auto-trade');
    if (upgradeAutoBtn) {
        upgradeAutoBtn.onclick = () => {
            if (gameState.money >= 30 && !gameState.upgrades.autoTrade) {
                gameState.money -= 30;
                gameState.upgrades.autoTrade = true;
                updateUI();
                showMessage('一键填写交割单已购买！', 'green');
            } else {
                showMessage('升级失败：金钱不足或已拥有', '#ff8888');
            }
        };
    }
    const tradeTypeSelect = document.getElementById('trade-type');
    if (tradeTypeSelect) {
        tradeTypeSelect.addEventListener('change', () => {
            const sellSelect = document.getElementById('sell-position-select');
            sellSelect.style.display = tradeTypeSelect.value === 'sell' ? 'inline-block' : 'none';
        });
    }
    const stockSelect = document.getElementById('stock-select');
    if (stockSelect) {
        stockSelect.addEventListener('change', () => updateStockUI());
    }
}

// ==================== 开局故事翻页 ====================
let storyPages = [
    "同志，您好！我们检查了你的学生会笔试与面试成绩，很明显，符合标准，你现在正式成为了学生会纪检部成员。",
    "您的任务简报：前往学校大门检查站，核查进出学生的证件。",
    "校长在动员会上强调：“校园安全重于泰山，每一张学生证都要仔细核对。”祝您工作顺利！"
];
let currentPage = 0;

function showStory(callback) {
    const modal = document.getElementById('story-modal');
    const contentDiv = document.getElementById('story-content');
    const prevBtn = document.getElementById('story-prev');
    const nextBtn = document.getElementById('story-next');
    const pageNumSpan = document.getElementById('story-page-num');
    
    currentPage = 0;
    function updatePage() {
        contentDiv.innerText = storyPages[currentPage];
        pageNumSpan.innerText = `${currentPage+1}/${storyPages.length}`;
        prevBtn.disabled = (currentPage === 0);
        nextBtn.innerText = (currentPage === storyPages.length-1) ? "开始游戏" : "下一页";
    }
    updatePage();
    
    const onPrev = () => {
        if (currentPage > 0) {
            currentPage--;
            updatePage();
        }
    };
    const onNext = () => {
        if (currentPage < storyPages.length-1) {
            currentPage++;
            updatePage();
        } else {
            modal.style.display = 'none';
            prevBtn.removeEventListener('click', onPrev);
            nextBtn.removeEventListener('click', onNext);
            if (callback) callback();
        }
    };
    prevBtn.addEventListener('click', onPrev);
    nextBtn.addEventListener('click', onNext);
    
    modal.style.display = 'flex';
}

// ==================== 注册面板 ====================
function showRegister(callback) {
    const modal = document.getElementById('register-modal');
    const input = document.getElementById('player-name-input');
    const confirmBtn = document.getElementById('register-confirm');
    input.value = '';
    modal.style.display = 'flex';
    const onConfirm = () => {
        let name = input.value.trim();
        if (name === '') name = '检察员';
        gameState.playerName = name;
        modal.style.display = 'none';
        confirmBtn.removeEventListener('click', onConfirm);
        if (callback) callback();
    };
    confirmBtn.addEventListener('click', onConfirm);
}

// ==================== 天赋选择 ====================
function showTalentSelection(callback) {
    const modal = document.getElementById('talent-modal');
    const economicBtn = document.getElementById('talent-economic');
    const justiceBtn = document.getElementById('talent-justice');
    const insightBtn = document.getElementById('talent-insight');
    
    const onSelect = (talent) => {
        gameState.talent = talent;
        modal.style.display = 'none';
        economicBtn.removeEventListener('click', () => onSelect('economic'));
        justiceBtn.removeEventListener('click', () => onSelect('justice'));
        insightBtn.removeEventListener('click', () => onSelect('insight'));
        if (callback) callback();
    };
    
    economicBtn.onclick = () => onSelect('economic');
    justiceBtn.onclick = () => onSelect('justice');
    insightBtn.onclick = () => onSelect('insight');
    
    modal.style.display = 'flex';
}

// ==================== 事件绑定与初始化 ====================
function bindEvents() {
    document.getElementById('btn-compare').onclick = () => {
        if (gameState.compareMode) {
            exitCompareMode();
            showMessage('对比模式已关闭', '#ffffa0');
        } else {
            enterCompareMode();
        }
    };
    document.getElementById('btn-approve').onclick = () => {
        if (!gameState.canCheck) return;
        if (gameState.currentVisitor) checkVisitor(gameState.currentVisitor, true);
    };
    document.getElementById('btn-reject').onclick = () => {
        if (!gameState.canCheck) return;
        if (gameState.currentVisitor) checkVisitor(gameState.currentVisitor, false);
    };
    document.getElementById('btn-arrest').onclick = () => {
        if (!gameState.canCheck) return;
        arrestVisitor();
    };
    document.getElementById('btn-confiscate').onclick = () => {
        if (!gameState.canCheck) return;
        confiscateItem();
    };
    document.getElementById('save-btn').onclick = saveGame;
    document.getElementById('load-btn').onclick = loadGame;
    document.getElementById('close-mailbox').onclick = () => {
        document.getElementById('mailbox-modal').style.display = 'none';
    };
    document.getElementById('close-achievements').onclick = () => {
        document.getElementById('achievements-modal').style.display = 'none';
    };
    document.getElementById('btn-next-student').onclick = callNextStudent;
    
    initComputer();
}

function startNewGame() {
    const simpleModeCheckbox = document.getElementById('simple-mode-checkbox');
    gameState = {
        day: 1,
        money: 0,
        timeLeft: 300,
        timerInterval: null,
        currentVisitor: null,
        visitedToday: 0,
        totalVisitorsToday: 10,
        upgrades: {
            quickBookmarks: false,
            advancedDorm: false,
            stickyNote: false,
            autoTrade: false
        },
        confiscatedItems: [],
        helpCount: 0,
        corruption: 0,
        route: null,
        simpleMode: simpleModeCheckbox.checked,
        phoneCallActive: false,
        phoneCallback: null,
        newspaperShownToday: false,
        hasFakeLetter: false,
        hasTicket: false,
        escapeReady: false,
        gameDate: new Date(2026, 2, 1),
        tutorialShown: false,
        compareMode: false,
        compareFirstField: null,
        day25EventTriggered: false,
        phoneConfirmedForged: false,
        mails: [],
        nextMailId: 1,
        phoneNumbers: generatePhoneNumbers(),
        wantedList: [],
        stocks: [
            { name: "实验科技", code: "SY001", price: 5.00, prevPrice: 5.00, positions: [] },
            { name: "深中贸易", code: "SZ002", price: 8.50, prevPrice: 8.50, positions: [] },
            { name: "深高级制造", code: "SG003", price: 12.00, prevPrice: 12.00, positions: [] },
            { name: "实验金融", code: "SY004", price: 9.50, prevPrice: 9.50, positions: [] },
            { name: "深外基建", code: "SW005", price: 7.50, prevPrice: 7.50, positions: [] }
        ],
        stockNews: "",
        lastStockUpdateDay: 0,
        trainingCompleted: false,
        playerName: "检察员",
        talent: null,
        achievements: {
            firstArrest: false,
            firstPhoneCall: false,
            firstStockTrade: false,
            firstHelpOrganization: false,
            firstConfiscation: false,
            firstTenCorrect: false,
            millionaire: false,
            perfectDay: false,
            stockMaster: false,
            undercover: false,
            whistleblower: false,
            survivalist: false,
            fugitive: false,
            revolutionary: false,
            loyalist: false,
            confiscator: false,
            corrupt: false
        },
        correctCount: 0,
        totalEarned: 0,
        stockProfit: 0,
        compareUsed: false,
        confiscatedNormalLetters: 0,
        escapePlanAvailable: false,
        canCheck: true
    };
    triggeredEvents = [];
    showTalentSelection(() => {
        applyTalent();
        showRegister(() => {
            document.getElementById('start-screen').style.display = 'none';
            document.getElementById('game-container').style.display = 'flex';
            bindEvents();
            gameState.newspaperShownToday = false;
            showStory(() => {
                startNewDay();
            });
        });
    });
}

function continueGame() {
    const simpleModeCheckbox = document.getElementById('simple-mode-checkbox');
    gameState.simpleMode = simpleModeCheckbox.checked;
    loadGame();
    document.getElementById('start-screen').style.display = 'none';
    document.getElementById('game-container').style.display = 'flex';
    bindEvents();
}

function saveGame() {
    const saveData = {
        day: gameState.day,
        money: gameState.money,
        timeLeft: gameState.timeLeft,
        visitedToday: gameState.visitedToday,
        totalVisitorsToday: gameState.totalVisitorsToday,
        upgrades: gameState.upgrades,
        confiscatedItems: gameState.confiscatedItems,
        helpCount: gameState.helpCount,
        corruption: gameState.corruption,
        simpleMode: gameState.simpleMode,
        hasFakeLetter: gameState.hasFakeLetter,
        hasTicket: gameState.hasTicket,
        escapeReady: gameState.escapeReady,
        triggeredEvents: triggeredEvents,
        newspaperShownToday: gameState.newspaperShownToday,
        gameDate: gameState.gameDate.toISOString(),
        tutorialShown: gameState.tutorialShown,
        day25EventTriggered: gameState.day25EventTriggered,
        mails: gameState.mails,
        nextMailId: gameState.nextMailId,
        phoneNumbers: gameState.phoneNumbers,
        stocks: gameState.stocks,
        stockNews: gameState.stockNews,
        lastStockUpdateDay: gameState.lastStockUpdateDay,
        trainingCompleted: gameState.trainingCompleted,
        playerName: gameState.playerName,
        talent: gameState.talent,
        achievements: gameState.achievements,
        correctCount: gameState.correctCount,
        totalEarned: gameState.totalEarned,
        stockProfit: gameState.stockProfit,
        compareUsed: gameState.compareUsed,
        confiscatedNormalLetters: gameState.confiscatedNormalLetters,
        escapePlanAvailable: gameState.escapePlanAvailable,
        canCheck: true
    };
    localStorage.setItem('studentGameSave', JSON.stringify(saveData));
    showMessage('游戏已保存！', '#88aa88');
}

function loadGame() {
    const raw = localStorage.getItem('studentGameSave');
    if (!raw) {
        showMessage('没有找到存档文件', '#ff8888');
        return;
    }
    try {
        const data = JSON.parse(raw);
        gameState.day = data.day;
        gameState.money = data.money;
        gameState.timeLeft = data.timeLeft;
        gameState.visitedToday = data.visitedToday;
        gameState.totalVisitorsToday = data.totalVisitorsToday;
        gameState.upgrades = data.upgrades;
        gameState.confiscatedItems = data.confiscatedItems;
        gameState.helpCount = data.helpCount;
        gameState.corruption = data.corruption || 0;
        gameState.simpleMode = data.simpleMode;
        gameState.hasFakeLetter = data.hasFakeLetter || false;
        gameState.hasTicket = data.hasTicket || false;
        gameState.escapeReady = data.escapeReady || false;
        triggeredEvents = data.triggeredEvents || [];
        gameState.newspaperShownToday = data.newspaperShownToday || false;
        gameState.gameDate = new Date(data.gameDate);
        gameState.tutorialShown = data.tutorialShown || false;
        gameState.day25EventTriggered = data.day25EventTriggered || false;
        gameState.mails = data.mails || [];
        gameState.nextMailId = data.nextMailId || 1;
        gameState.phoneNumbers = data.phoneNumbers || null;
        gameState.stocks = data.stocks || [
            { name: "实验科技", code: "SY001", price: 5.00, prevPrice: 5.00, positions: [] },
            { name: "深中贸易", code: "SZ002", price: 8.50, prevPrice: 8.50, positions: [] },
            { name: "深高级制造", code: "SG003", price: 12.00, prevPrice: 12.00, positions: [] },
            { name: "实验金融", code: "SY004", price: 9.50, prevPrice: 9.50, positions: [] },
            { name: "深外基建", code: "SW005", price: 7.50, prevPrice: 7.50, positions: [] }
        ];
        gameState.stockNews = data.stockNews || "";
        gameState.lastStockUpdateDay = data.lastStockUpdateDay || 0;
        gameState.trainingCompleted = data.trainingCompleted || false;
        gameState.playerName = data.playerName || "检察员";
        gameState.talent = data.talent || null;
        gameState.achievements = data.achievements || {
            firstArrest: false,
            firstPhoneCall: false,
            firstStockTrade: false,
            firstHelpOrganization: false,
            firstConfiscation: false,
            firstTenCorrect: false,
            millionaire: false,
            perfectDay: false,
            stockMaster: false,
            undercover: false,
            whistleblower: false,
            survivalist: false,
            fugitive: false,
            revolutionary: false,
            loyalist: false,
            confiscator: false,
            corrupt: false
        };
        gameState.correctCount = data.correctCount || 0;
        gameState.totalEarned = data.totalEarned || 0;
        gameState.stockProfit = data.stockProfit || 0;
        gameState.compareUsed = data.compareUsed || false;
        gameState.confiscatedNormalLetters = data.confiscatedNormalLetters || 0;
        gameState.escapePlanAvailable = data.escapePlanAvailable || false;
        gameState.canCheck = true;
        
        if (gameState.timerInterval) clearInterval(gameState.timerInterval);
        gameState.currentVisitor = generateVisitor();
        displayVisitor(gameState.currentVisitor);
        gameState.timerInterval = setInterval(() => {
            if (gameState.timeLeft <= 1) {
                clearInterval(gameState.timerInterval);
                endDay();
            } else {
                gameState.timeLeft--;
                document.getElementById('time-left').innerText = formatTime(gameState.timeLeft);
            }
        }, 1000);
        
        updateUI();
        updateMailIcon();
        showMessage('读取存档成功！', '#88aa88');
    } catch(e) {
        console.error(e);
        showMessage('读取失败，存档损坏', '#ff8888');
    }
}

// ==================== 作弊菜单（内置，按 Ctrl+Shift+C 或 F12 打开） ====================
(function() {
    let cheatMenuVisible = false;
    let cheatMenu = null;
    let statusPanelVisible = false;
    let statusPanel = null;

    function createCheatMenu() {
        if (cheatMenu) return;

        cheatMenu = document.createElement('div');
        cheatMenu.id = 'cheat-menu';
        cheatMenu.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: #1e2a1c;
            border: 2px solid #7a6a4a;
            padding: 20px;
            z-index: 9999;
            font-family: 'Courier New', monospace;
            color: #b8d0a8;
            max-height: 80vh;
            overflow-y: auto;
            width: 440px;
            display: none;
            box-shadow: 0 0 20px rgba(0,0,0,0.8);
            border-radius: 8px;
        `;
        cheatMenu.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #7a6a4a; padding-bottom: 8px; margin-bottom: 12px;">
                <h3 style="margin: 0; color: #ffcc00;">🛠 作弊菜单</h3>
                <button id="cheat-close-btn" style="background: #8a3a2a; border: none; color: white; padding: 4px 12px; cursor: pointer; font-size: 16px;">✕</button>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px;">
                <button class="cheat-btn" data-action="money1000">💰 +1000元</button>
                <button class="cheat-btn" data-action="money10000">💰 +10000元</button>
                <button class="cheat-btn" data-action="day20">📅 跳到第20天</button>
                <button class="cheat-btn" data-action="day25">📅 跳到第25天</button>
                <button class="cheat-btn" data-action="allAch">🏆 解锁全部成就</button>
                <button class="cheat-btn" data-action="train">✅ 完成培训</button>
                <button class="cheat-btn" data-action="escape">🏃 帮助逃跑者</button>
                <button class="cheat-btn" data-action="confiscate">📑 没收介绍信+1</button>
                <button class="cheat-btn" data-action="plan">🚀 开启逃亡计划</button>
                <button class="cheat-btn" data-action="fakeLetter">📄 伪造介绍信</button>
                <button class="cheat-btn" data-action="realLetter">📄 正常介绍信</button>
                <button class="cheat-btn" data-action="helpOrg">🕊️ 帮助组织+5</button>
                <button class="cheat-btn" data-action="corrupt">☠️ 腐败+1</button>
                <button class="cheat-btn" data-action="escapeEnd">🏃 直接逃亡结局</button>
                <button class="cheat-btn" data-action="nextDay">⏩ 结束今天</button>
                <button class="cheat-btn" data-action="fullStatus">📊 查看状态面板</button>
                <button class="cheat-btn" data-action="day3">📧 触发第3天邮件</button>
                <button class="cheat-btn" data-action="reset">🔄 重置游戏</button>
            </div>
            <div style="margin-top: 10px; font-size: 11px; color: #7a8a6a; border-top: 1px solid #3a4a3a; padding-top: 6px;">
                快捷键: Ctrl+Shift+C 或 F12 切换菜单
            </div>
        `;

        const style = document.createElement('style');
        style.textContent = `
            .cheat-btn {
                background: #2c4a3a;
                border: 1px outset #6a9a6a;
                color: #c0e0c0;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                padding: 6px 8px;
                cursor: pointer;
                text-align: center;
                border-radius: 4px;
            }
            .cheat-btn:hover {
                background: #3a5a4a;
            }
            .cheat-btn:active {
                border: 1px inset #6a9a6a;
                transform: translate(1px,1px);
            }
        `;
        document.head.appendChild(style);

        cheatMenu.querySelector('#cheat-close-btn').onclick = () => {
            cheatMenu.style.display = 'none';
            cheatMenuVisible = false;
        };

        cheatMenu.addEventListener('click', (e) => {
            const btn = e.target.closest('.cheat-btn');
            if (!btn) return;
            const action = btn.dataset.action;
            if (action === 'fullStatus') {
                showStatusPanel();
                return;
            }
            executeCheat(action);
        });

        document.body.appendChild(cheatMenu);
    }

    // 状态面板
    function showStatusPanel() {
        if (statusPanel) {
            statusPanel.style.display = 'block';
            updateStatusPanelContent();
            return;
        }

        statusPanel = document.createElement('div');
        statusPanel.id = 'status-panel';
        statusPanel.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: #1a2a1a;
            border: 2px solid #7a6a4a;
            padding: 20px;
            z-index: 10000;
            font-family: 'Courier New', monospace;
            color: #c0d8b0;
            max-height: 80vh;
            overflow-y: auto;
            width: 480px;
            box-shadow: 0 0 30px rgba(0,0,0,0.9);
            border-radius: 8px;
        `;

        const closeBtn = document.createElement('button');
        closeBtn.innerText = '✕ 关闭';
        closeBtn.style.cssText = `
            background: #8a3a2a;
            border: none;
            color: white;
            padding: 4px 16px;
            cursor: pointer;
            font-size: 14px;
            float: right;
            border-radius: 4px;
        `;
        closeBtn.onclick = () => {
            statusPanel.style.display = 'none';
        };

        statusPanel.appendChild(closeBtn);

        const title = document.createElement('h3');
        title.innerText = '📊 游戏状态面板';
        title.style.cssText = 'margin-top: 0; color: #ffcc00; border-bottom: 1px solid #3a5a3a; padding-bottom: 8px;';
        statusPanel.appendChild(title);

        const content = document.createElement('div');
        content.id = 'status-panel-content';
        statusPanel.appendChild(content);

        document.body.appendChild(statusPanel);
        updateStatusPanelContent();
    }

    function updateStatusPanelContent() {
        const content = document.getElementById('status-panel-content');
        if (!content) return;

        const totalAch = Object.keys(gameState.achievements).length;
        const unlockedAch = Object.values(gameState.achievements).filter(v => v).length;

        let visitorInfo = '无';
        if (gameState.currentVisitor) {
            const v = gameState.currentVisitor;
            const hasLetter = v.transferLetter ? '有' : '无';
            const isForged = v.transferLetter?.forged ? '（伪造）' : v.transferLetter ? '（正常）' : '';
            visitorInfo = `${v.name} | ${v.school} | ${v.grade}年级 | 介绍信: ${hasLetter} ${isForged}`;
        }

        let stockInfo = '无';
        const positions = gameState.stocks.filter(s => s.positions.length > 0);
        if (positions.length > 0) {
            stockInfo = positions.map(s => {
                const pos = s.positions.map(p => `${p.shares}份@${p.openPrice.toFixed(2)}x${p.leverage}`).join(', ');
                return `${s.name}: ${pos}`;
            }).join(' | ');
        }

        let confiscatedInfo = '无';
        if (gameState.confiscatedItems.length > 0) {
            confiscatedInfo = gameState.confiscatedItems.map(item => `${item.name}(${item.school})`).join(', ');
        }

        content.innerHTML = `
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 4px 12px; font-size: 13px; line-height: 1.6;">
                <div><strong>📅 天数</strong></div><div>${gameState.day} / 30</div>
                <div><strong>💰 金钱</strong></div><div>${gameState.money.toFixed(2)} 元</div>
                <div><strong>⏱️ 剩余时间</strong></div><div>${formatTime(gameState.timeLeft)}</div>
                <div><strong>📋 今日已查</strong></div><div>${gameState.visitedToday} / ${gameState.totalVisitorsToday}</div>
                <div><strong>🕊️ 帮助组织</strong></div><div>${gameState.helpCount} 次</div>
                <div><strong>🏃 帮助逃跑者</strong></div><div>${gameState.escapeReady ? '✅ 是' : '❌ 否'}</div>
                <div><strong>📑 没收正常介绍信</strong></div><div>${gameState.confiscatedNormalLetters} 次</div>
                <div><strong>🏆 成就进度</strong></div><div>${unlockedAch} / ${totalAch}</div>
                <div><strong>✅ 培训完成</strong></div><div>${gameState.trainingCompleted ? '✅ 是' : '❌ 否'}</div>
                <div><strong>🎯 天赋</strong></div><div>${gameState.talent || '未选择'}</div>
                <div><strong>☠️ 腐败值</strong></div><div>${gameState.corruption}</div>
                <div><strong>📄 当前访客</strong></div><div style="font-size: 11px;">${visitorInfo}</div>
                <div><strong>📊 股票持仓</strong></div><div style="font-size: 11px;">${stockInfo}</div>
                <div><strong>📦 没收物品</strong></div><div style="font-size: 11px;">${confiscatedInfo}</div>
                <div><strong>📝 升级</strong></div><div>${Object.entries(gameState.upgrades).filter(([k,v]) => v).map(([k]) => k).join(', ') || '无'}</div>
                <div><strong>🏃 逃亡计划可用</strong></div><div>${gameState.escapePlanAvailable ? '✅ 是' : '❌ 否'}</div>
            </div>
            <div style="margin-top: 12px; padding-top: 8px; border-top: 1px solid #3a5a3a; font-size: 11px; color: #8aa88a;">
                <span>💡 点击右上角 ✕ 关闭此面板</span>
            </div>
        `;
    }

    function executeCheat(action) {
        switch(action) {
            case 'money1000':
                gameState.money += 1000;
                updateUI();
                showMessage('💰 +1000 元', '#ffcc00', 1500);
                break;
            case 'money10000':
                gameState.money += 10000;
                updateUI();
                showMessage('💰 +10000 元', '#ffcc00', 1500);
                break;
            case 'day20':
                gameState.day = 20;
                gameState.newspaperShownToday = false;
                updateUI();
                startNewDay();
                showMessage('📅 跳转到第 20 天', '#ffcc00', 1500);
                break;
            case 'day25':
                gameState.day = 25;
                gameState.day25EventTriggered = false;
                gameState.visitedToday = 0;
                gameState.newspaperShownToday = false;
                updateUI();
                startNewDay();
                showMessage('📅 跳转到第 25 天（逃跑者将在第一个访客出现）', '#ffcc00', 2500);
                break;
            case 'allAch':
                Object.keys(gameState.achievements).forEach(k => gameState.achievements[k] = true);
                updateUI();
                showMessage('🏆 所有成就已解锁', '#ffcc00', 1500);
                break;
            case 'train':
                gameState.trainingCompleted = true;
                updateUI();
                showMessage('✅ 培训已完成', '#88ff88', 1500);
                break;
            case 'escape':
                gameState.escapeReady = true;
                showMessage('🏃 已标记为帮助过逃跑者', '#ffcc00', 1500);
                break;
            case 'confiscate':
                gameState.confiscatedNormalLetters += 1;
                showMessage(`📑 没收正常介绍信次数：${gameState.confiscatedNormalLetters}`, '#ffcc00', 1500);
                break;
            case 'plan':
                gameState.escapeReady = true;
                gameState.confiscatedNormalLetters = 1;
                gameState.money = 300;
                updateUI();
                startNewDay();
                showMessage('🚀 逃亡计划已就绪，状态栏将显示按钮', '#ffcc00', 2500);
                break;
            case 'fakeLetter':
                if (gameState.currentVisitor) {
                    gameState.currentVisitor.transferLetter = {
                        name: gameState.currentVisitor.name,
                        studentId: gameState.currentVisitor.studentId,
                        fromSchool: '深圳中学',
                        toSchool: '深圳实验中学',
                        signatures: { fromPrincipal: '李华', toPrincipal: '王明' },
                        forged: true
                    };
                    gameState.currentVisitor.documents.push('transferLetter');
                    gameState.currentVisitor.forged = true;
                    gameState.currentVisitor.forgedDocs.push('transferLetter');
                    gameState.currentVisitor.purpose = '转学';
                    displayVisitor(gameState.currentVisitor);
                    updateUI();
                    showMessage('📄 已添加伪造介绍信', '#ff8888', 1500);
                } else {
                    showMessage('❌ 没有当前访客', '#ff8888', 1500);
                }
                break;
            case 'realLetter':
                if (gameState.currentVisitor) {
                    gameState.currentVisitor.transferLetter = {
                        name: gameState.currentVisitor.name,
                        studentId: gameState.currentVisitor.studentId,
                        fromSchool: '深圳中学',
                        toSchool: '深圳实验中学',
                        signatures: { fromPrincipal: '李华', toPrincipal: '王明' },
                        forged: false
                    };
                    gameState.currentVisitor.documents.push('transferLetter');
                    gameState.currentVisitor.purpose = '转学';
                    displayVisitor(gameState.currentVisitor);
                    updateUI();
                    showMessage('📄 已添加正常介绍信', '#88ff88', 1500);
                } else {
                    showMessage('❌ 没有当前访客', '#ff8888', 1500);
                }
                break;
            case 'helpOrg':
                gameState.helpCount += 5;
                updateUI();
                showMessage('🕊️ 帮助组织次数 +5', '#ffcc00', 1500);
                break;
            case 'corrupt':
                gameState.corruption += 1;
                showMessage(`☠️ 腐败值 +1，当前腐败值：${gameState.corruption}`, '#ff4444', 2000);
                break;
            case 'escapeEnd':
                if (gameState.timerInterval) clearInterval(gameState.timerInterval);
                showEnding('逃亡结局', '你使用作弊菜单直接触发了逃亡结局。你带着伪造的证件和车票逃离了深圳，开始了新生活...', {
                    money: Math.floor(gameState.money),
                    day: gameState.day,
                    correct: gameState.correctCount
                });
                break;
            case 'nextDay':
                if (gameState.timerInterval) clearInterval(gameState.timerInterval);
                endDay();
                showMessage('⏩ 已结束今天', '#ffcc00', 1500);
                break;
            case 'day3':
                gameState.day = 3;
                gameState.newspaperShownToday = false;
                updateUI();
                startNewDay();
                showMessage('📧 第3天已开始，组织事件邮件即将到来', '#ffcc00', 2000);
                break;
            case 'reset':
                if (confirm('确定要重置游戏吗？所有进度将丢失。')) {
                    localStorage.removeItem('studentGameSave');
                    location.reload();
                }
                break;
            default:
                showMessage('❌ 未知作弊指令', '#ff8888', 1500);
        }
    }

    function toggleCheatMenu() {
        createCheatMenu();
        cheatMenuVisible = !cheatMenuVisible;
        cheatMenu.style.display = cheatMenuVisible ? 'block' : 'none';
        if (cheatMenuVisible) {
            updateUI();
        }
    }

    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey && e.shiftKey && (e.key === 'c' || e.key === 'C')) || (e.key === 'F12')) {
            e.preventDefault();
            toggleCheatMenu();
        }
    });

    console.log('🛠 作弊菜单已加载，按 Ctrl+Shift+C 或 F12 打开');
    console.log('📊 点击“查看状态面板”可查看所有游戏数据');
})();

window.gameState = gameState;